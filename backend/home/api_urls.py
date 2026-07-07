from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import (
    BannerViewSet, FacilityViewSet, HomePageView,
    CategoryProductsView, ProductDetailView
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'banners', BannerViewSet, basename='banner')
router.register(r'facilities', FacilityViewSet, basename='facility')

urlpatterns = [
    # Homepage and product views
    path('homepage/', HomePageView.as_view(), name='homepage'),
    path('category/<str:category_name>/', CategoryProductsView.as_view(), name='category-products'),
    path('category/<str:category_name>/<str:product_slug>/', ProductDetailView.as_view(), name='product-detail'),
    
    # Include router URLs
    path('', include(router.urls)),
]