from rest_framework import serializers
from .models import Banner, Facility
from products.serializers import CategorySerializer
from users.serializers import UserSerializer


class BannerSerializer(serializers.ModelSerializer):
    """Serializer for Banner model"""
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Banner
        fields = [
            'id', 'title', 'subtitle', 'description', 'image', 'image_url',
            'user', 'category', 'category_id', 'type', 'active'
        ]
        read_only_fields = ['id', 'user']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class BannerCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Banner create/update operations"""
    class Meta:
        model = Banner
        fields = [
            'title', 'subtitle', 'description', 'image', 
            'category', 'type', 'active'
        ]
    
    def validate_title(self, value):
        # Check if title is unique (excluding current instance for updates)
        queryset = Banner.objects.filter(title=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError('Banner with this title already exists.')
        return value


class FacilitySerializer(serializers.ModelSerializer):
    """Serializer for Facility model"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Facility
        fields = ['id', 'image', 'image_url', 'title', 'active']
        read_only_fields = ['id']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class FacilityCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Facility create/update operations"""
    class Meta:
        model = Facility
        fields = ['image', 'title', 'active']


class HomePageDataSerializer(serializers.Serializer):
    """Serializer for homepage data"""
    banners = serializers.DictField()
    latest_products = serializers.ListField()
    special_offers = serializers.DictField()
    hot_deals = serializers.ListField()
    categories = serializers.ListField()
    blogs = serializers.ListField()
    facilities = serializers.ListField()