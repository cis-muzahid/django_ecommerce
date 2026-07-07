from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F
from decimal import Decimal

from .models import Cart, Wishlist
from products.models import Product
from .serializers import (
    CartSerializer, CartCreateUpdateSerializer, WishlistSerializer,
    WishlistCreateSerializer, CartSummarySerializer, WishlistSummarySerializer
)


class CartViewSet(ModelViewSet):
    """ViewSet for Cart management"""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Users can only access their own cart items"""
        return Cart.objects.filter(user=self.request.user, active=True).order_by('-id')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CartCreateUpdateSerializer
        return CartSerializer
    
    def create(self, request, *args, **kwargs):
        """Add item to cart or update quantity if already exists"""
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id, is_delete=False)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product does not exist'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if item already exists in cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            active=True,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if item already exists
            cart_item.quantity += quantity
            cart_item.save()
            message = f'{product.name} quantity updated in cart'
        else:
            message = f'{product.name} added to cart successfully'
        
        serializer = CartSerializer(cart_item, context={'request': request})
        return Response({
            'message': message,
            'item': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """Update cart item quantity"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Ensure user can only update their own cart items
        if instance.user != request.user:
            return Response(
                {'error': 'You can only update your own cart items'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': 'Cart item updated successfully',
            'item': CartSerializer(instance, context={'request': request}).data
        })
    
    def destroy(self, request, *args, **kwargs):
        """Remove item from cart (soft delete)"""
        cart_item = self.get_object()
        
        # Ensure user can only delete their own cart items
        if cart_item.user != request.user:
            return Response(
                {'error': 'You can only delete your own cart items'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        cart_item.active = False
        cart_item.save()
        
        return Response({
            'message': 'Item removed from cart successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get cart summary with total items and amount"""
        cart_items = self.get_queryset()
        
        total_items = cart_items.count()
        total_amount = sum(
            item.product.price * item.quantity for item in cart_items
        )
        
        serializer = CartSummarySerializer({
            'total_items': total_items,
            'total_amount': total_amount,
            'items': cart_items
        }, context={'request': request})
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Clear all items from cart"""
        cart_items = self.get_queryset()
        cart_items.update(active=False)
        
        return Response({
            'message': 'Cart cleared successfully'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def increase_quantity(self, request, pk=None):
        """Increase item quantity by 1"""
        cart_item = self.get_object()
        
        if cart_item.user != request.user:
            return Response(
                {'error': 'You can only update your own cart items'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        cart_item.quantity += 1
        cart_item.save()
        
        serializer = CartSerializer(cart_item, context={'request': request})
        return Response({
            'message': 'Quantity increased successfully',
            'item': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def decrease_quantity(self, request, pk=None):
        """Decrease item quantity by 1"""
        cart_item = self.get_object()
        
        if cart_item.user != request.user:
            return Response(
                {'error': 'You can only update your own cart items'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            
            serializer = CartSerializer(cart_item, context={'request': request})
            return Response({
                'message': 'Quantity decreased successfully',
                'item': serializer.data
            })
        else:
            # If quantity is 1, remove the item
            cart_item.active = False
            cart_item.save()
            
            return Response({
                'message': 'Item removed from cart'
            }, status=status.HTTP_204_NO_CONTENT)


class WishlistViewSet(ModelViewSet):
    """ViewSet for Wishlist management"""
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Users can only access their own wishlist items"""
        return Wishlist.objects.filter(user=self.request.user, active=True).order_by('-id')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return WishlistCreateSerializer
        return WishlistSerializer
    
    def create(self, request, *args, **kwargs):
        """Add item to wishlist"""
        product_id = request.data.get('product')
        
        try:
            product = Product.objects.get(id=product_id, is_delete=False)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product does not exist'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if item already exists in wishlist
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product,
            active=True
        )
        
        if not created:
            return Response({
                'message': 'Product is already in your wishlist'
            }, status=status.HTTP_200_OK)
        
        serializer = WishlistSerializer(wishlist_item, context={'request': request})
        return Response({
            'message': f'{product.name} added to wishlist successfully',
            'item': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        """Remove item from wishlist (soft delete)"""
        wishlist_item = self.get_object()
        
        # Ensure user can only delete their own wishlist items
        if wishlist_item.user != request.user:
            return Response(
                {'error': 'You can only delete your own wishlist items'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        wishlist_item.active = False
        wishlist_item.save()
        
        return Response({
            'message': 'Item removed from wishlist successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get wishlist summary"""
        wishlist_items = self.get_queryset()
        
        serializer = WishlistSummarySerializer({
            'total_items': wishlist_items.count(),
            'items': wishlist_items
        }, context={'request': request})
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Clear all items from wishlist"""
        wishlist_items = self.get_queryset()
        wishlist_items.update(active=False)
        
        return Response({
            'message': 'Wishlist cleared successfully'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def move_to_cart(self, request, pk=None):
        """Move item from wishlist to cart"""
        wishlist_item = self.get_object()
        
        if wishlist_item.user != request.user:
            return Response(
                {'error': 'You can only move your own wishlist items'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Add to cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=wishlist_item.product,
            active=True,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        # Remove from wishlist
        wishlist_item.active = False
        wishlist_item.save()
        
        cart_serializer = CartSerializer(cart_item, context={'request': request})
        return Response({
            'message': f'{wishlist_item.product.name} moved to cart successfully',
            'cart_item': cart_serializer.data
        }, status=status.HTTP_200_OK)


class CartWishlistStatsView(APIView):
    """API view for cart and wishlist statistics"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get cart and wishlist counts"""
        cart_count = Cart.objects.filter(user=request.user, active=True).count()
        wishlist_count = Wishlist.objects.filter(user=request.user, active=True).count()
        
        cart_total = sum(
            item.product.price * item.quantity 
            for item in Cart.objects.filter(user=request.user, active=True)
        )
        
        return Response({
            'cart': {
                'count': cart_count,
                'total_amount': float(cart_total)
            },
            'wishlist': {
                'count': wishlist_count
            }
        })