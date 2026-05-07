from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .api_views import (
    BlogCategoryViewSet, BlogViewSet, CommentViewSet,
    BlogSearchView, BlogDetailBySlugView
)

# Create main router
router = DefaultRouter()
router.register(r'categories', BlogCategoryViewSet, basename='blog-category')
router.register(r'blogs', BlogViewSet, basename='blog')

# Create nested router for blog comments
blogs_router = routers.NestedDefaultRouter(router, r'blogs', lookup='blog')
blogs_router.register(r'comments', CommentViewSet, basename='blog-comments')

urlpatterns = [
    # Search and detail endpoints
    path('blogs/search/', BlogSearchView.as_view(), name='blog-search'),
    path('blogs/slug/<str:slug>/', BlogDetailBySlugView.as_view(), name='blog-detail-by-slug'),
    
    # Include router URLs
    path('', include(router.urls)),
    path('', include(blogs_router.urls)),
]