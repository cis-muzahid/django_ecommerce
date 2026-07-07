from rest_framework import serializers
from .models import Cart, Wishlist
from products.serializers import ProductListSerializer
from users.serializers import UserSerializer


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model"""
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'product', 'product_id', 'quantity', 
            'active', 'total_price'
        ]
        read_only_fields = ['id', 'user', 'active']
    
    def get_total_price(self, obj):
        return float(obj.product.price * obj.quantity)
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('Quantity must be greater than 0')
        return value
    
    def validate_product_id(self, value):
        from products.models import Product
        try:
            product = Product.objects.get(id=value, is_delete=False)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product does not exist')
        return value


class CartCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Cart create/update operations"""
    class Meta:
        model = Cart
        fields = ['product', 'quantity']
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('Quantity must be greater than 0')
        return value


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for Wishlist model"""
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_id', 'active']
        read_only_fields = ['id', 'user', 'active']
    
    def validate_product_id(self, value):
        from products.models import Product
        try:
            product = Product.objects.get(id=value, is_delete=False)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product does not exist')
        return value


class WishlistCreateSerializer(serializers.ModelSerializer):
    """Serializer for Wishlist create operations"""
    class Meta:
        model = Wishlist
        fields = ['product']


class CartSummarySerializer(serializers.Serializer):
    """Serializer for cart summary"""
    total_items = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    items = CartSerializer(many=True)


class WishlistSummarySerializer(serializers.Serializer):
    """Serializer for wishlist summary"""
    total_items = serializers.IntegerField()
    items = WishlistSerializer(many=True)