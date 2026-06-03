from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .api_views import (
    CategoryViewSet, ProductViewSet, ProductAttributeViewSet,
    ProductSpecificationViewSet, ProductReviewViewSet, ProductSearchView,
    UserProductReviewsView
)

# Create main router
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

# Create nested routers for product-related resources
products_router = routers.NestedDefaultRouter(router, r'products', lookup='product')
products_router.register(r'attributes', ProductAttributeViewSet, basename='product-attributes')
products_router.register(r'specifications', ProductSpecificationViewSet, basename='product-specifications')
products_router.register(r'reviews', ProductReviewViewSet, basename='product-reviews')

urlpatterns = [
    # Search endpoint
    path('products/search/', ProductSearchView.as_view(), name='product-search'),
    path('reviews/my/', UserProductReviewsView.as_view(), name='my-product-reviews'),
    
    # Include router URLs
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]
