from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from django.utils import timezone
import stripe
from django.conf import settings

from .models import Order, OrderItem, ReturnAndReplaceOrder
from cart.models import Cart
from users.models import UserAddress
from .serializers import (
    OrderSerializer, OrderCreateSerializer, OrderItemSerializer,
    ReturnAndReplaceOrderSerializer, ReturnAndReplaceCreateSerializer,
    OrderStatusUpdateSerializer, PaymentIntentSerializer,
    OrderTrackingSerializer, OrderSummarySerializer
)
from .utilities import order_cart_item, check_default_address, fetch_user_address

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderViewSet(ModelViewSet):
    """ViewSet for Order management"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'payment_status']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Users can only access their own orders"""
        user = self.request.user
        queryset = Order.objects.filter(user=user)
        
        # Admin and suppliers can see all orders
        if hasattr(user, 'user_role') and user.user_role:
            if user.user_role.name in ['admin'] or user.is_superuser:
                queryset = Order.objects.all()
            elif user.user_role.name == 'supplier':
                # Suppliers can see orders for their products
                queryset = Order.objects.filter(
                    orderitem__cart__product__user=user
                ).distinct()
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new order"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            order = serializer.save()
            order_serializer = OrderSerializer(order, context={'request': request})
            
            return Response({
                'message': 'Order created successfully',
                'order': order_serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        
        if order.user != request.user:
            return Response(
                {'error': 'You can only cancel your own orders'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if order.status in ['deliverd', 'cancelled']:
            return Response(
                {'error': 'Cannot cancel this order'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cancel order items
        OrderItem.objects.filter(order=order).update(active=False)
        order.status = 'cancelled'
        order.save()
        
        # Process refund if payment was made
        if order.payment_id and order.payment_status == 'succeeded':
            try:
                refund = stripe.Refund.create(
                    payment_intent=order.payment_id,
                    amount=int(float(order.total_amount) * 100),  # Convert to cents
                )
                return Response({
                    'message': 'Order cancelled and refund processed successfully'
                }, status=status.HTTP_200_OK)
            except stripe.error.StripeError as e:
                return Response({
                    'message': 'Order cancelled but refund failed',
                    'error': str(e)
                }, status=status.HTTP_200_OK)
        
        return Response({
            'message': 'Order cancelled successfully'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update order status (Admin/Supplier only)"""
        order = self.get_object()
        
        # Check permissions
        if not (hasattr(request.user, 'user_role') and request.user.user_role):
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.user.user_role.name not in ['admin', 'supplier'] and not request.user.is_superuser:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = OrderStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            order.status = serializer.validated_data['status']
            order.save()
            
            return Response({
                'message': 'Order status updated successfully',
                'order': OrderSerializer(order, context={'request': request}).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get order summary for the user"""
        user = request.user
        orders = Order.objects.filter(user=user)
        
        summary_data = {
            'total_orders': orders.count(),
            'pending_orders': orders.filter(status='initial').count(),
            'delivered_orders': orders.filter(status='deliverd').count(),
            'cancelled_orders': orders.filter(status='cancelled').count(),
            'total_amount_spent': orders.aggregate(
                total=Sum('total_amount')
            )['total'] or 0
        }
        
        serializer = OrderSummarySerializer(summary_data)
        return Response(serializer.data)


class CheckoutView(APIView):
    """API view for checkout process"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get checkout information"""
        user = request.user
        
        # Get cart items
        cart_items = Cart.objects.filter(user=user, active=True)
        if not cart_items.exists():
            return Response({
                'error': 'Cart is empty'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate totals
        total_amount = sum(
            item.product.price * item.quantity for item in cart_items
        )
        
        # Get addresses
        addresses = fetch_user_address(user)
        default_address = check_default_address(user)
        
        from cart.serializers import CartSerializer
        return Response({
            'cart_items': CartSerializer(cart_items, many=True, context={'request': request}).data,
            'total_amount': float(total_amount),
            'addresses': [
                {
                    'id': addr.id,
                    'street': addr.street,
                    'city': addr.city,
                    'state': addr.state,
                    'postal_code': addr.postal_code,
                    'country': addr.country,
                    'is_default': addr.is_default
                } for addr in addresses
            ] if addresses else [],
            'default_address': {
                'id': default_address.id,
                'street': default_address.street,
                'city': default_address.city,
                'state': default_address.state,
                'postal_code': default_address.postal_code,
                'country': default_address.country,
            } if default_address else None
        })
    
    def post(self, request):
        """Process checkout and create order"""
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                order = serializer.save()
                order_serializer = OrderSerializer(order, context={'request': request})
                
                return Response({
                    'message': 'Order created successfully',
                    'order': order_serializer.data
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentView(APIView):
    """API view for payment processing"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Create payment intent for Stripe"""
        serializer = PaymentIntentSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            payment_method = serializer.validated_data['payment_method']
            order_id = serializer.validated_data.get('order_id')
            
            if order_id:
                order = get_object_or_404(Order, id=order_id, user=user)
                total_amount = order.total_amount
            else:
                # Get cart items and calculate total before an order has been created.
                cart_items = Cart.objects.filter(user=user, active=True)
                if not cart_items.exists():
                    return Response({
                        'error': 'Cart is empty'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                total_amount = sum(
                    item.product.price * item.quantity for item in cart_items
                )
            
            if payment_method == 'stripe':
                try:
                    # Create Stripe payment intent
                    intent = stripe.PaymentIntent.create(
                        amount=int(float(total_amount) * 100),  # Convert to cents
                        currency='usd',  # You can make this configurable
                        metadata={
                            'user_id': user.id,
                            'user_email': user.email,
                            'order_id': order_id or ''
                        }
                    )
                    
                    return Response({
                        'client_secret': intent.client_secret,
                        'payment_intent_id': intent.id,
                        'amount': float(total_amount)
                    })
                    
                except stripe.error.StripeError as e:
                    return Response({
                        'error': str(e)
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response({
                    'error': 'Unsupported payment method'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReturnAndReplaceViewSet(ModelViewSet):
    """ViewSet for Return and Replace requests"""
    serializer_class = ReturnAndReplaceOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['action', 'requested', 'approved', 'active']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Users can only access their own return/replace requests"""
        user = self.request.user
        queryset = ReturnAndReplaceOrder.objects.filter(user=user, active=True)
        
        # Admin and suppliers can see all requests
        if hasattr(user, 'user_role') and user.user_role:
            if user.user_role.name in ['admin'] or user.is_superuser:
                queryset = ReturnAndReplaceOrder.objects.filter(active=True)
            elif user.user_role.name == 'supplier':
                # Suppliers can see requests for their products
                queryset = ReturnAndReplaceOrder.objects.filter(
                    order__cart__product__user=user,
                    active=True
                )
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReturnAndReplaceCreateSerializer
        return ReturnAndReplaceOrderSerializer
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve return/replace request (Admin/Supplier only)"""
        return_replace = self.get_object()
        
        # Check permissions
        if not (hasattr(request.user, 'user_role') and request.user.user_role):
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.user.user_role.name not in ['admin', 'supplier'] and not request.user.is_superuser:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return_replace.approved = True
        return_replace.save()
        
        # Process refund for returns
        if return_replace.action == 'Return':
            order = return_replace.order.order
            if order.payment_id and order.payment_status == 'succeeded':
                try:
                    stripe.Refund.create(
                        payment_intent=order.payment_id,
                        amount=int(float(return_replace.order.cart.product.price) * 100),
                    )
                except stripe.error.StripeError:
                    pass  # Handle refund error silently for now
        
        return Response({
            'message': f'{return_replace.action} request approved successfully'
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel return/replace request"""
        return_replace = self.get_object()
        
        if return_replace.user != request.user:
            return Response(
                {'error': 'You can only cancel your own requests'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return_replace.active = False
        return_replace.save()
        
        return Response({
            'message': 'Request cancelled successfully'
        })


class OrderTrackingView(APIView):
    """API view for order tracking"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Track order by ID"""
        serializer = OrderTrackingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            order = Order.objects.get(id=order_id, user=request.user)
            
            order_items = OrderItem.objects.filter(order=order, active=True)
            
            return Response({
                'order': OrderSerializer(order, context={'request': request}).data,
                'order_items': OrderItemSerializer(order_items, many=True).data,
                'tracking_info': {
                    'status': order.status,
                    'created_at': order.created_at,
                    'updated_at': order.updated_at,
                    'estimated_delivery': None  # You can add delivery estimation logic
                }
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
