from rest_framework import serializers
from decimal import Decimal
from .models import Order, OrderItem, ReturnAndReplaceOrder, PaymentEvent
from .utilities import cancel_stale_pending_orders, finalize_order_carts, ONLINE_PAYMENT_METHODS
from cart.models import Cart
from cart.serializers import CartSerializer
from users.serializers import UserSerializer, UserAddressSerializer
from users.models import UserAddress


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model"""
    cart = CartSerializer(read_only=True)
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'cart', 'active', 'product_name', 
            'product_price', 'total_price'
        ]
        read_only_fields = ['id']
    
    def get_product_name(self, obj):
        return obj.cart.product.name if obj.cart else None
    
    def get_product_price(self, obj):
        return float(obj.cart.product.price) if obj.cart else 0
    
    def get_total_price(self, obj):
        if obj.cart:
            return float(obj.cart.product.price * obj.cart.quantity)
        return 0


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model"""
    user = UserSerializer(read_only=True)
    order_items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'active', 'status', 'total_amount', 'address',
            'payment_method', 'payment_id', 'payment_status', 'created_at',
            'updated_at', 'order_items', 'items_count'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_items_count(self, obj):
        return obj.orderitem_set.filter(active=True).count()


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for Order creation"""
    address_id = serializers.IntegerField(required=False)
    payment_method = serializers.CharField(max_length=255, default='none')
    
    class Meta:
        model = Order
        fields = ['address_id', 'payment_method']
    
    def validate_address_id(self, value):
        if value:
            try:
                address = UserAddress.objects.get(
                    id=value, 
                    user=self.context['request'].user
                )
                return value
            except UserAddress.DoesNotExist:
                raise serializers.ValidationError('Invalid address selected')
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        address_id = validated_data.pop('address_id', None)
        payment_method = validated_data.get('payment_method', 'none')

        if payment_method in ONLINE_PAYMENT_METHODS:
            cancel_stale_pending_orders(user)

        # Get user's cart items
        cart_items = Cart.objects.filter(user=user, active=True)
        if not cart_items.exists():
            raise serializers.ValidationError('Cart is empty')
        
        # Calculate total amount
        total_amount = sum(
            item.product.price * item.quantity for item in cart_items
        )
        
        # Get address
        address_text = "No address provided"
        if address_id:
            try:
                address = UserAddress.objects.get(id=address_id, user=user)
                address_text = f"{address.street}, {address.city}, {address.state}, {address.postal_code}, {address.country}"
            except UserAddress.DoesNotExist:
                pass
        else:
            # Use default address if available
            default_address = UserAddress.objects.filter(user=user, is_default=True).first()
            if default_address:
                address_text = f"{default_address.street}, {default_address.city}, {default_address.state}, {default_address.postal_code}, {default_address.country}"
        
        order_kwargs = dict(validated_data)
        if payment_method in ONLINE_PAYMENT_METHODS:
            order_kwargs['payment_status'] = 'pending'
            order_kwargs['active'] = False
        elif payment_method == 'none':
            # COD: payment not yet collected, will be collected at delivery
            order_kwargs['payment_status'] = 'cod_pending'

        # Create order
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            address=address_text,
            **order_kwargs,
        )
        
        # Link cart items to the order; only clear cart after payment (or immediately for COD)
        for cart_item in cart_items:
            OrderItem.objects.create(order=order, cart=cart_item)

        if payment_method == 'none':
            finalize_order_carts(order)

        return order


class ReturnAndReplaceOrderSerializer(serializers.ModelSerializer):
    """Serializer for ReturnAndReplaceOrder model"""
    order = OrderItemSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    cart = CartSerializer(read_only=True)
    payment_method = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    order_id = serializers.SerializerMethodField()

    class Meta:
        model = ReturnAndReplaceOrder
        fields = [
            'id', 'order', 'requested', 'approved', 'reason', 'action',
            'created_at', 'updated_at', 'cart', 'user', 'active',
            'payment_method', 'payment_status', 'order_id',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_payment_method(self, obj):
        try:
            return obj.order.order.payment_method
        except Exception:
            return None

    def get_payment_status(self, obj):
        try:
            return obj.order.order.payment_status
        except Exception:
            return None

    def get_order_id(self, obj):
        try:
            return obj.order.order.id
        except Exception:
            return None


class ReturnAndReplaceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating return/replace requests"""
    order_item_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ReturnAndReplaceOrder
        fields = ['order_item_id', 'reason', 'action']
    
    def validate_action(self, value):
        if value not in ['Return', 'Replace']:
            raise serializers.ValidationError('Action must be either "Return" or "Replace"')
        return value
    
    def validate_order_item_id(self, value):
        try:
            order_item = OrderItem.objects.get(
                id=value,
                order__user=self.context['request'].user,
                active=True
            )
            return value
        except OrderItem.DoesNotExist:
            raise serializers.ValidationError('Invalid order item')
    
    def create(self, validated_data):
        user = self.context['request'].user
        order_item_id = validated_data.pop('order_item_id')
        order_item = OrderItem.objects.get(id=order_item_id)
        
        return ReturnAndReplaceOrder.objects.create(
            order=order_item,
            user=user,
            requested=True,
            **validated_data
        )


class OrderStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating order status"""
    status = serializers.ChoiceField(choices=Order.ORDER_STATUS)


class PaymentIntentSerializer(serializers.Serializer):
    """Serializer for payment intent creation"""
    payment_method = serializers.CharField(max_length=50)
    address_id = serializers.IntegerField(required=False)
    order_id = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)


class OrderTrackingSerializer(serializers.Serializer):
    """Serializer for order tracking"""
    order_id = serializers.IntegerField()
    
    def validate_order_id(self, value):
        try:
            order = Order.objects.get(
                id=value,
                user=self.context['request'].user
            )
            return value
        except Order.DoesNotExist:
            raise serializers.ValidationError('Order not found')


class OrderSummarySerializer(serializers.Serializer):
    """Serializer for order summary"""
    total_orders = serializers.IntegerField()
    pending_orders = serializers.IntegerField()
    delivered_orders = serializers.IntegerField()
    cancelled_orders = serializers.IntegerField()
    total_amount_spent = serializers.DecimalField(max_digits=10, decimal_places=2)


class PaymentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentEvent
        fields = [
            'id', 'order', 'stripe_event_id', 'event_type', 'payment_intent_id',
            'payment_status', 'amount', 'currency', 'payload', 'created_at'
        ]
