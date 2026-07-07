from rest_framework import serializers
from .models import Blog, BlogCategory, Comment
from users.serializers import UserSerializer


class BlogCategorySerializer(serializers.ModelSerializer):
    """Serializer for BlogCategory model"""
    user = UserSerializer(read_only=True)
    blog_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'user', 'active', 'blog_count']
        read_only_fields = ['id', 'user']
    
    def get_blog_count(self, obj):
        return Blog.objects.filter(category=obj, active=True).count()


class BlogCategoryCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for BlogCategory create/update operations"""
    class Meta:
        model = BlogCategory
        fields = ['name', 'active']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    user = UserSerializer(read_only=True)
    user_name = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'description', 'user', 'user_name', 'parent_comment',
            'active', 'created_at', 'updated_at', 'replies'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.email
    
    def get_replies(self, obj):
        if obj.parent_comment is None:  # Only get replies for parent comments
            replies = Comment.objects.filter(parent_comment=obj, active=True)
            return CommentSerializer(replies, many=True, context=self.context).data
        return []


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Comment create/update operations"""
    class Meta:
        model = Comment
        fields = ['description', 'parent_comment']


class BlogListSerializer(serializers.ModelSerializer):
    """Serializer for Blog list view (minimal data)"""
    user = UserSerializer(read_only=True)
    category = BlogCategorySerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'excerpt', 'image', 'image_url', 'user',
            'slug', 'category', 'active', 'created_at', 'updated_at',
            'comment_count'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_comment_count(self, obj):
        return Comment.objects.filter(blog=obj, active=True).count()
    
    def get_excerpt(self, obj):
        # Return first 150 characters of description
        return obj.description[:150] + '...' if len(obj.description) > 150 else obj.description


class BlogDetailSerializer(serializers.ModelSerializer):
    """Serializer for Blog detail view (complete data)"""
    user = UserSerializer(read_only=True)
    category = BlogCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    image_url = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'description', 'image', 'image_url', 'user',
            'slug', 'category', 'category_id', 'active', 'created_at',
            'updated_at', 'comments', 'comment_count'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_comments(self, obj):
        # Get only parent comments (replies are nested within them)
        comments = Comment.objects.filter(
            blog=obj, active=True, parent_comment=None
        ).order_by('-created_at')
        return CommentSerializer(comments, many=True, context=self.context).data
    
    def get_comment_count(self, obj):
        return Comment.objects.filter(blog=obj, active=True).count()


class BlogCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Blog create/update operations"""
    class Meta:
        model = Blog
        fields = ['title', 'description', 'image', 'slug', 'category', 'active']
    
    def validate_title(self, value):
        # Check if title is unique (excluding current instance for updates)
        queryset = Blog.objects.filter(title=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError('Blog with this title already exists.')
        return value
    
    def validate_slug(self, value):
        # Check if slug is unique (excluding current instance for updates)
        queryset = Blog.objects.filter(slug=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError('Blog with this slug already exists.')
        return value