from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Avg
from django.shortcuts import get_object_or_404

from .models import Category, Product, ProductAttribute, ProductSpecification, ProductReview
from .serializers import (
    CategorySerializer, CategoryCreateUpdateSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductCreateUpdateSerializer,
    ProductAttributeSerializer, ProductAttributeCreateUpdateSerializer,
    ProductSpecificationSerializer, ProductSpecificationCreateUpdateSerializer,
    ProductReviewSerializer, ProductReviewCreateUpdateSerializer
)


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
        """Get all active parent categories with nested subcategories."""
        def build_category_tree(category):
            children = Category.objects.filter(parent_category=category, is_delete=False).order_by('name')
            return {
                'id': category.id,
                'name': category.name,
                'parent_category': None if category.parent_category is None else {
                    'id': category.parent_category.id,
                    'name': category.parent_category.name,
                },
                'subcategories': [build_category_tree(child) for child in children],
                'product_count': Product.objects.filter(category=category, is_delete=False).count(),
            }

        categories = Category.objects.filter(parent_category=None, is_delete=False).order_by('name')
        return Response([build_category_tree(category) for category in categories])
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get products in a specific category"""
        category = self.get_object()
        products = Product.objects.filter(category=category, is_delete=False)
        
        # Apply filters
        search = request.query_params.get('search')
        if search:
            products = products.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        # Apply ordering
        ordering = request.query_params.get('ordering', '-created_at')
        products = products.order_by(ordering)
        
        # Paginate
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(ModelViewSet):
    """ViewSet for Product management"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'tag', 'price']
    search_fields = ['name', 'description', 'tag']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_delete=False)
        
        # Filter by user role for suppliers
        if hasattr(self.request.user, 'user_role') and self.request.user.user_role:
            if self.request.user.user_role.name == 'supplier':
                queryset = queryset.filter(user=self.request.user)
        
        # Price range filter
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete product"""
        product = self.get_object()
        product.is_delete = True
        product.save()
        return Response({'message': 'Product deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products (products with HOT tag)"""
        products = Product.objects.filter(is_delete=False, tag='HOT')[:10]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest products"""
        products = Product.objects.filter(is_delete=False).order_by('-created_at')[:10]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        """Get related products (same category)"""
        product = self.get_object()
        related_products = Product.objects.filter(
            category=product.category, is_delete=False
        ).exclude(id=product.id)[:5]
        
        serializer = ProductListSerializer(related_products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductAttributeViewSet(ModelViewSet):
    """ViewSet for ProductAttribute management"""
    serializer_class = ProductAttributeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        return ProductAttribute.objects.filter(product_id=product_id, is_delete=False)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductAttributeCreateUpdateSerializer
        return ProductAttributeSerializer
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(product=product)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete product attribute"""
        attribute = self.get_object()
        attribute.is_delete = True
        attribute.save()
        return Response({'message': 'Product attribute deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)


class ProductSpecificationViewSet(ModelViewSet):
    """ViewSet for ProductSpecification management"""
    serializer_class = ProductSpecificationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        return ProductSpecification.objects.filter(product_id=product_id, is_delete=False)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductSpecificationCreateUpdateSerializer
        return ProductSpecificationSerializer
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(product=product)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete product specification"""
        specification = self.get_object()
        specification.is_delete = True
        specification.save()
        return Response({'message': 'Product specification deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)


class ProductReviewViewSet(ModelViewSet):
    """ViewSet for ProductReview management"""
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    ordering = ['-created_at']
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        return ProductReview.objects.filter(product_id=product_id)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductReviewCreateUpdateSerializer
        return ProductReviewSerializer

    def create(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_pk')
        product = get_object_or_404(Product, id=product_id)

        existing_review = ProductReview.objects.filter(
            product=product, user=request.user
        ).first()

        if existing_review:
            return Response(
                {'error': 'You have already reviewed this product'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(product=product, user=self.request.user)
    
    def get_permissions(self):
        """Only authenticated users can create/update/delete reviews"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        
        return [permission() for permission in permission_classes]
    
    def update(self, request, *args, **kwargs):
        """Only allow users to update their own reviews"""
        review = self.get_object()
        if review.user != request.user:
            return Response(
                {'error': 'You can only update your own reviews'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Only allow users to delete their own reviews"""
        review = self.get_object()
        if review.user != request.user:
            return Response(
                {'error': 'You can only delete your own reviews'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class UserProductReviewsView(APIView):
    """API view for the current user's product reviews."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        reviews = ProductReview.objects.filter(user=request.user).order_by('-created_at')
        serializer = ProductReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)


class ProductSearchView(APIView):
    """Advanced product search API"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        category_id = request.query_params.get('category')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        tag = request.query_params.get('tag')
        sort_by = request.query_params.get('sort_by', '-created_at')
        
        products = Product.objects.filter(is_delete=False)
        
        # Text search
        if query:
            products = products.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(tag__icontains=query)
            )
        
        # Category filter
        if category_id:
            products = products.filter(category_id=category_id)
        
        # Price range filter
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        
        # Tag filter
        if tag:
            products = products.filter(tag=tag)
        
        # Sorting
        if sort_by in ['name', '-name', 'price', '-price', 'created_at', '-created_at']:
            products = products.order_by(sort_by)
        
        # Pagination
        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(products, request)
        
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
