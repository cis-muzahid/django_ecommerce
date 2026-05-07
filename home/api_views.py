from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Banner, Facility
from products.models import Product, Category
from blog.models import Blog
from .serializers import (
    BannerSerializer, BannerCreateUpdateSerializer,
    FacilitySerializer, FacilityCreateUpdateSerializer,
    HomePageDataSerializer
)
from products.serializers import ProductListSerializer, CategorySerializer
from blog.serializers import BlogListSerializer
from .utilities import (
    fetch_all_categories, hot_deals_product, fetch_banner,
    fetch_category_product, fetch_categories
)


class BannerViewSet(ModelViewSet):
    """ViewSet for Banner management"""
    queryset = Banner.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'category', 'active']
    search_fields = ['title', 'subtitle', 'description']
    ordering_fields = ['title', 'id']
    ordering = ['-id']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BannerCreateUpdateSerializer
        return BannerSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete banner"""
        banner = self.get_object()
        banner.active = False
        banner.save()
        return Response({'message': 'Banner deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get banners grouped by type"""
        banner_types = Banner.objects.filter(active=True).values_list('type', flat=True).distinct()
        
        result = {}
        for banner_type in banner_types:
            banners = Banner.objects.filter(type=banner_type, active=True).order_by('-id')
            result[banner_type] = BannerSerializer(
                banners, many=True, context={'request': request}
            ).data
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def header_banners(self, request):
        """Get header banners"""
        banners = Banner.objects.filter(type='header banner', active=True).order_by('-id')
        serializer = BannerSerializer(banners, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def middle_banners(self, request):
        """Get middle banners"""
        banners = Banner.objects.filter(type='middle banner', active=True).order_by('-id')[:3]
        serializer = BannerSerializer(banners, many=True, context={'request': request})
        return Response(serializer.data)


class FacilityViewSet(ModelViewSet):
    """ViewSet for Facility management"""
    queryset = Facility.objects.filter(active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title', 'id']
    ordering = ['-id']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FacilityCreateUpdateSerializer
        return FacilitySerializer
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete facility"""
        facility = self.get_object()
        facility.active = False
        facility.save()
        return Response({'message': 'Facility deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)


class HomePageView(APIView):
    """API view for homepage data"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """Get all homepage data"""
        # Get banners
        banners = Banner.objects.filter(active=True).order_by('-id')
        banner_data = {
            'header_banners': BannerSerializer(
                banners.filter(type='header banner'), 
                many=True, context={'request': request}
            ).data,
            'wide_banner_large': BannerSerializer(
                banners.filter(type='wide banner large').first(), 
                context={'request': request}
            ).data if banners.filter(type='wide banner large').exists() else None,
            'wide_banner_small': BannerSerializer(
                banners.filter(type='wide banner small').first(), 
                context={'request': request}
            ).data if banners.filter(type='wide banner small').exists() else None,
            'middle_banners': BannerSerializer(
                banners.filter(type='middle banner')[:3], 
                many=True, context={'request': request}
            ).data,
        }
        
        # Get products
        products = Product.objects.filter(is_delete=False).order_by('-id')
        hot_deals = hot_deals_product()[:3]
        
        # Get categories
        categories = fetch_all_categories()
        
        # Get blogs
        blogs = Blog.objects.filter(active=True)[:5]
        
        # Get facilities
        facilities = Facility.objects.filter(active=True).order_by('-id')
        
        data = {
            'banners': banner_data,
            'latest_products': ProductListSerializer(
                products, many=True, context={'request': request}
            ).data,
            'special_offers': {
                'products_1': ProductListSerializer(
                    products[:3], many=True, context={'request': request}
                ).data,
                'products_2': ProductListSerializer(
                    products[3:6], many=True, context={'request': request}
                ).data,
                'products_3': ProductListSerializer(
                    products[6:9], many=True, context={'request': request}
                ).data,
            },
            'hot_deals': ProductListSerializer(
                hot_deals, many=True, context={'request': request}
            ).data,
            'categories': CategorySerializer(
                categories, many=True, context={'request': request}
            ).data,
            'blogs': BlogListSerializer(
                blogs, many=True, context={'request': request}
            ).data,
            'facilities': FacilitySerializer(
                facilities, many=True, context={'request': request}
            ).data,
        }
        
        return Response(data)


class CategoryProductsView(APIView):
    """API view for category products"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, category_name):
        """Get products by category"""
        try:
            category = Category.objects.get(name=category_name, is_delete=False)
        except Category.DoesNotExist:
            return Response({
                'error': 'Category not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get category hierarchy
        categories = fetch_categories(category)
        products = fetch_category_product(categories).order_by('-id')
        
        # Apply filters
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        search = request.query_params.get('search')
        
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if search:
            products = products.filter(name__icontains=search)
        
        # Get banner for category
        banner = fetch_banner(category)
        
        # Pagination
        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(products, request)
        
        if page is not None:
            product_serializer = ProductListSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response({
                'products': product_serializer.data,
                'category': CategorySerializer(category, context={'request': request}).data,
                'banner': BannerSerializer(banner, context={'request': request}).data if banner else None,
                'all_categories': CategorySerializer(
                    fetch_all_categories(), many=True, context={'request': request}
                ).data
            })
        
        return Response({
            'products': ProductListSerializer(products, many=True, context={'request': request}).data,
            'category': CategorySerializer(category, context={'request': request}).data,
            'banner': BannerSerializer(banner, context={'request': request}).data if banner else None,
            'all_categories': CategorySerializer(
                fetch_all_categories(), many=True, context={'request': request}
            ).data
        })
    
    def post(self, request, category_name):
        """Filter products by price range"""
        try:
            category = Category.objects.get(name=category_name, is_delete=False)
        except Category.DoesNotExist:
            return Response({
                'error': 'Category not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        price_range = request.data.get('price', '').split(',')
        if len(price_range) == 2:
            try:
                min_price, max_price = float(price_range[0]), float(price_range[1])
                categories = fetch_categories(category)
                products = fetch_category_product(categories).filter(
                    price__range=(min_price, max_price)
                ).order_by('-id')
                
                return Response({
                    'products': ProductListSerializer(
                        products, many=True, context={'request': request}
                    ).data,
                    'category': CategorySerializer(category, context={'request': request}).data,
                    'all_categories': CategorySerializer(
                        fetch_all_categories(), many=True, context={'request': request}
                    ).data
                })
            except ValueError:
                return Response({
                    'error': 'Invalid price range'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'error': 'Price range required'
        }, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """API view for product details"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, category_name, product_slug):
        """Get product details"""
        try:
            category = Category.objects.get(name=category_name, is_delete=False)
            product = Product.objects.get(slug=product_slug, category=category, is_delete=False)
        except (Category.DoesNotExist, Product.DoesNotExist):
            return Response({
                'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get related data
        banner = fetch_banner(category)
        hot_deals = hot_deals_product().filter(category=category)[:3]
        related_products = Product.objects.filter(
            category=category, is_delete=False
        ).exclude(id=product.id)[:5]
        categories = fetch_all_categories()
        
        from products.serializers import ProductDetailSerializer
        
        return Response({
            'product': ProductDetailSerializer(product, context={'request': request}).data,
            'category': CategorySerializer(category, context={'request': request}).data,
            'banner': BannerSerializer(banner, context={'request': request}).data if banner else None,
            'hot_deals': ProductListSerializer(
                hot_deals, many=True, context={'request': request}
            ).data,
            'related_products': ProductListSerializer(
                related_products, many=True, context={'request': request}
            ).data,
            'categories': CategorySerializer(
                categories, many=True, context={'request': request}
            ).data
        })