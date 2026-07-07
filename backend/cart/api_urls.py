from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import CartViewSet, WishlistViewSet, CartWishlistStatsView

# Create router for ViewSets
router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = [
    # Statistics endpoint
    path('cart-wishlist-stats/', CartWishlistStatsView.as_view(), name='cart-wishlist-stats'),
    
    # Include router URLs
    path('', include(router.urls)),
]