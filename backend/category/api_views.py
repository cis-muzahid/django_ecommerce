from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from products.models import Category, Product
from .serializers import (
    CategorySerializer, CategoryCreateUpdateSerializer, CategoryTreeSerializer
)
from products.serializers import ProductListSerializer


class CategoryViewSet(ModelViewSet):
    """ViewSet for Category management"""
    queryset = Category.objects.filter(is_delete=False)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['parent_category']
    search_fields = ['name']
    ordering_fields = ['name', 'id']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CategoryCreateUpdateSerializer
        return CategorySerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete category"""
        category = self.get_object()
        
        # Check if category has products
        product_count = Product.objects.filter(category=category, is_delete=False).count()
        if product_count > 0:
            return Response({
                'error': f'Cannot delete category. It has {product_count} products.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if category has subcategories
        subcategory_count = Category.objects.filter(parent_category=category, is_delete=False).count()
        if subcategory_count > 0:
            return Response({
                'error': f'Cannot delete category. It has {subcategory_count} subcategories.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        category.is_delete = True
        category.save()
        return Response({'message': 'Category deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def parent_categories(self, request):
        """Get all parent categories (categories without parent)"""
        categories = Category.objects.filter(parent_category=None, is_delete=False)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        """Get subcategories of a specific category"""
        category = self.get_object()
        subcategories = Category.objects.filter(parent_category=category, is_delete=False)
        serializer = self.get_serializer(subcategories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """Get category tree structure"""
        parent_categories = Category.objects.filter(parent_category=None, is_delete=False)
        serializer = CategoryTreeSerializer(parent_categories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get products in a specific category and its subcategories"""
        category = self.get_object()
        
        # Get all descendant categories
        def get_all_descendants(cat):
            descendants = [cat]
            children = Category.objects.filter(parent_category=cat, is_delete=False)
            for child in children:
                descendants.extend(get_all_descendants(child))
            return descendants
        
        all_categories = get_all_descendants(category)
        category_ids = [cat.id for cat in all_categories]
        
        products = Product.objects.filter(category_id__in=category_ids, is_delete=False)
        
        # Apply filters
        search = request.query_params.get('search')
        if search:
            products = products.filter(name__icontains=search)
        
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        
        tag = request.query_params.get('tag')
        if tag:
            products = products.filter(tag=tag)
        
        # Apply ordering
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering in ['name', '-name', 'price', '-price', 'created_at', '-created_at']:
            products = products.order_by(ordering)
        
        # Paginate
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def breadcrumb(self, request, pk=None):
        """Get category breadcrumb path"""
        category = self.get_object()
        breadcrumb = []
        
        current = category
        while current:
            breadcrumb.insert(0, {
                'id': current.id,
                'name': current.name
            })
            current = current.parent_category
        
        return Response({
            'breadcrumb': breadcrumb,
            'category': CategorySerializer(category, context={'request': request}).data
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get category statistics"""
        total_categories = Category.objects.filter(is_delete=False).count()
        parent_categories = Category.objects.filter(parent_category=None, is_delete=False).count()
        categories_with_products = Category.objects.filter(
            is_delete=False,
            product__is_delete=False
        ).distinct().count()
        
        return Response({
            'total_categories': total_categories,
            'parent_categories': parent_categories,
            'categories_with_products': categories_with_products,
            'empty_categories': total_categories - categories_with_products
        })