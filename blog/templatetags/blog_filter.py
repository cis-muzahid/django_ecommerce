from django import template
from blog.models import BlogCategory, Blog
from products.models import Category
from django.db.models import Count

register = template.Library()

@register.filter
def blog_categories(a):
    """ filter to fetch blog's categories """
    return BlogCategory.objects.filter(active=True)

@register.filter
def product_categories(a):
    """ filter to fetch product's categories """
    return Category.objects.filter(is_delete=False)

@register.filter
def top_blogs_with_most_comments(a):
    """ filter to fetch most commented blog """
    blogs_with_comment_count = Blog.objects.annotate(comment_count=Count('comment')).order_by('-comment_count')
    top_two_blogs = blogs_with_comment_count.filter(active=True)[:2]    
    return top_two_blogs

@register.filter
def recently_created_blogs_view(a):
    """ filter to fetch recently created blog """
    return Blog.objects.filter(active=True).order_by('-created_at')[:2]