from rest_framework import serializers
from .models import Category, Product, ProductAttribute, ProductSpecification, ProductReview
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    parent_category = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'parent_category', 'subcategories', 
            'product_count', 'is_delete', 'user'
        ]
        read_only_fields = ['id', 'user']
    
    def get_parent_category(self, obj):
        if obj.parent_category:
            return {
                'id': obj.parent_category.id,
                'name': obj.parent_category.name
            }
        return None
    
    def get_subcategories(self, obj):
        subcategories = Category.objects.filter(parent_category=obj, is_delete=False)
        return [{'id': cat.id, 'name': cat.name} for cat in subcategories]
    
    def get_product_count(self, obj):
        return Product.objects.filter(category=obj, is_delete=False).count()


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Category create/update operations"""
    class Meta:
        model = Category
        fields = ['name', 'parent_category']
    
    def validate_name(self, value):
        if ' ' in value:
            raise serializers.ValidationError('Name should not contain spaces.')
        return value


class ProductAttributeSerializer(serializers.ModelSerializer):
    """Serializer for ProductAttribute model"""
    class Meta:
        model = ProductAttribute
        fields = [
            'id', 'title', 'value', 'product_image', 
            'out_of_stoke', 'is_display', 'is_delete'
        ]
        read_only_fields = ['id']


class ProductSpecificationSerializer(serializers.ModelSerializer):
    """Serializer for ProductSpecification model"""
    class Meta:
        model = ProductSpecification
        fields = ['id', 'title', 'description', 'is_delete']
        read_only_fields = ['id']


class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer for ProductReview model"""
    user = UserSerializer(read_only=True)
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductReview
        fields = [
            'id', 'review', 'title', 'comment', 'user', 'user_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.email


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for Product list view (minimal data)"""
    category = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'category', 'slug', 'tag',
            'average_rating', 'review_count', 'main_image', 'created_at'
        ]
    
    def get_category(self, obj):
        return {
            'id': obj.category.id,
            'name': obj.category.name
        }
    
    def get_average_rating(self, obj):
        reviews = ProductReview.objects.filter(product=obj)
        if reviews.exists():
            return round(sum(review.review for review in reviews) / reviews.count(), 1)
        return 0
    
    def get_review_count(self, obj):
        return ProductReview.objects.filter(product=obj).count()
    
    def get_main_image(self, obj):
        # Get the first product attribute with an image
        attribute = ProductAttribute.objects.filter(
            product=obj, product_image__isnull=False, is_delete=False
        ).first()
        if attribute and attribute.product_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(attribute.product_image.url)
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for Product detail view (complete data)"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    attributes = ProductAttributeSerializer(
        source='productattribute_set', many=True, read_only=True
    )
    specifications = ProductSpecificationSerializer(
        source='productspecification_set', many=True, read_only=True
    )
    reviews = ProductReviewSerializer(
        source='productreview_set', many=True, read_only=True
    )
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    available_variants = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'weight', 'length', 
            'width', 'height', 'tag', 'category', 'category_id', 'user', 
            'slug', 'is_delete', 'created_at', 'updated_at',
            'attributes', 'specifications', 'reviews', 'average_rating',
            'review_count', 'available_variants'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        reviews = obj.productreview_set.all()
        if reviews.exists():
            return round(sum(review.review for review in reviews) / reviews.count(), 1)
        return 0
    
    def get_review_count(self, obj):
        return obj.productreview_set.count()
    
    def get_available_variants(self, obj):
        """Get available product variants (attributes that are in stock)"""
        variants = ProductAttribute.objects.filter(
            product=obj, is_delete=False, is_display=True, out_of_stoke=False
        )
        return ProductAttributeSerializer(variants, many=True).data


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Product create/update operations"""
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'weight', 'length', 
            'width', 'height', 'tag', 'category', 'slug'
        ]
    
    def validate_slug(self, value):
        # Check if slug is unique (excluding current instance for updates)
        queryset = Product.objects.filter(slug=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError('Product with this slug already exists.')
        return value


class ProductAttributeCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for ProductAttribute create/update operations"""
    class Meta:
        model = ProductAttribute
        fields = [
            'title', 'value', 'product_image', 'out_of_stoke', 'is_display'
        ]


class ProductSpecificationCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for ProductSpecification create/update operations"""
    class Meta:
        model = ProductSpecification
        fields = ['title', 'description']


class ProductReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for ProductReview create/update operations"""
    class Meta:
        model = ProductReview
        fields = ['review', 'title', 'comment']
    
    def validate_review(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('Review rating must be between 1 and 5.')
        return value