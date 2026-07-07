from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import CategoryViewSet

# Create router for ViewSets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
]