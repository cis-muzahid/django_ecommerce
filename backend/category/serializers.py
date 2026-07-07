from rest_framework import serializers
from products.models import Category
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    parent_category = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    
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
        from products.models import Product
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
    
    def validate(self, attrs):
        # Prevent circular references
        parent_category = attrs.get('parent_category')
        if parent_category and self.instance:
            if parent_category == self.instance:
                raise serializers.ValidationError('Category cannot be its own parent.')
            
            # Check for circular reference in the hierarchy
            current_parent = parent_category
            while current_parent:
                if current_parent == self.instance:
                    raise serializers.ValidationError('Circular reference detected in category hierarchy.')
                current_parent = current_parent.parent_category
        
        return attrs


class CategoryTreeSerializer(serializers.ModelSerializer):
    """Serializer for Category tree structure"""
    children = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'product_count', 'children']
    
    def get_children(self, obj):
        children = Category.objects.filter(parent_category=obj, is_delete=False)
        return CategoryTreeSerializer(children, many=True).data
    
    def get_product_count(self, obj):
        from products.models import Product
        return Product.objects.filter(category=obj, is_delete=False).count()