from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404

from .models import Blog, BlogCategory, Comment
from .serializers import (
    BlogListSerializer, BlogDetailSerializer, BlogCreateUpdateSerializer,
    BlogCategorySerializer, BlogCategoryCreateUpdateSerializer,
    CommentSerializer, CommentCreateUpdateSerializer
)


class BlogCategoryViewSet(ModelViewSet):
    """ViewSet for BlogCategory management"""
    queryset = BlogCategory.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'id']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogCategoryCreateUpdateSerializer
        return BlogCategorySerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete blog category"""
        category = self.get_object()
        category.active = False
        category.save()
        return Response({'message': 'Blog category deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def blogs(self, request, pk=None):
        """Get blogs in a specific category"""
        category = self.get_object()
        blogs = Blog.objects.filter(category=category, active=True).order_by('-created_at')
        
        # Apply search filter
        search = request.query_params.get('search')
        if search:
            blogs = blogs.filter(title__icontains=search)
        
        # Paginate
        page = self.paginate_queryset(blogs)
        if page is not None:
            serializer = BlogListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = BlogListSerializer(blogs, many=True, context={'request': request})
        return Response(serializer.data)


class BlogViewSet(ModelViewSet):
    """ViewSet for Blog management"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'active']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Blog.objects.filter(active=True)
        
        # Filter by user role for content creators
        if hasattr(self.request.user, 'user_role') and self.request.user.user_role:
            if self.request.user.user_role.name not in ['admin'] and not self.request.user.is_superuser:
                # Non-admin users can only see their own blogs for editing
                if self.action in ['update', 'partial_update', 'destroy']:
                    queryset = queryset.filter(user=self.request.user)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BlogListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return BlogCreateUpdateSerializer
        return BlogDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete blog"""
        blog = self.get_object()
        
        # Check if user can delete this blog
        if blog.user != request.user and not request.user.is_superuser:
            if not (hasattr(request.user, 'user_role') and request.user.user_role and request.user.user_role.name == 'admin'):
                return Response(
                    {'error': 'You can only delete your own blogs'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        
        blog.active = False
        blog.save()
        return Response({'message': 'Blog deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest blogs"""
        blogs = Blog.objects.filter(active=True).order_by('-created_at')[:10]
        serializer = BlogListSerializer(blogs, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured blogs (you can add a featured field to the model)"""
        # For now, return latest blogs
        blogs = Blog.objects.filter(active=True).order_by('-created_at')[:5]
        serializer = BlogListSerializer(blogs, many=True, context={'request': request})
        return Response(serializer.data)


class CommentViewSet(ModelViewSet):
    """ViewSet for Comment management"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    ordering = ['-created_at']
    
    def get_queryset(self):
        blog_id = self.kwargs.get('blog_pk')
        return Comment.objects.filter(blog_id=blog_id, active=True)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentCreateUpdateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        blog_id = self.kwargs.get('blog_pk')
        blog = get_object_or_404(Blog, id=blog_id, active=True)
        serializer.save(blog=blog, user=self.request.user)
    
    def get_permissions(self):
        """Only authenticated users can create/update/delete comments"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        
        return [permission() for permission in permission_classes]
    
    def update(self, request, *args, **kwargs):
        """Only allow users to update their own comments"""
        comment = self.get_object()
        if comment.user != request.user:
            return Response(
                {'error': 'You can only update your own comments'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete comment - only allow users to delete their own comments"""
        comment = self.get_object()
        if comment.user != request.user:
            return Response(
                {'error': 'You can only delete your own comments'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        comment.active = False
        comment.save()
        return Response({'message': 'Comment deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)


class BlogSearchView(APIView):
    """Advanced blog search API"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        category_id = request.query_params.get('category')
        sort_by = request.query_params.get('sort_by', '-created_at')
        
        blogs = Blog.objects.filter(active=True)
        
        # Text search
        if query:
            blogs = blogs.filter(title__icontains=query)
        
        # Category filter
        if category_id:
            blogs = blogs.filter(category_id=category_id)
        
        # Sorting
        if sort_by in ['title', '-title', 'created_at', '-created_at']:
            blogs = blogs.order_by(sort_by)
        
        # Pagination
        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(blogs, request)
        
        if page is not None:
            serializer = BlogListSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = BlogListSerializer(blogs, many=True, context={'request': request})
        return Response(serializer.data)


class BlogDetailBySlugView(APIView):
    """Get blog by slug"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, slug):
        try:
            blog = Blog.objects.get(slug=slug, active=True)
            serializer = BlogDetailSerializer(blog, context={'request': request})
            return Response(serializer.data)
        except Blog.DoesNotExist:
            return Response(
                {'error': 'Blog not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )