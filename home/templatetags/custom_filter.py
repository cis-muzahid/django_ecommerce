from django import template
from django.shortcuts import get_object_or_404
from products.models import ProductAttribute, Product, Category
from cart.models import Cart

register = template.Library()

@register.filter
def subcategories(category):
    subcategories = Category.objects.filter(parent_category=category)
    return subcategories

@register.filter
def product_attributes(product_id):
    """fetching product attributes"""
    product_attribute = ProductAttribute.objects.filter(title__icontains='color',product=product_id).first()
    return product_attribute.product_image

@register.filter
def product_filter(category):
    categories = Category.objects.filter(parent_category=category).values_list('id', flat=True)
    subcategory = Category.objects.filter(parent_category__in=categories).values_list('id', flat=True)
    products = Product.objects.filter(category__in=subcategory).order_by('-id')
    return products

@register.filter
def electronics_product_filter(category):
    category = get_object_or_404(Category, name__icontains=category)
    return product_filter(category.id)

@register.filter
def fetch_all_parent_category(category):
    categories = []
    while category is not None:
        if category.parent_category != None:
            categories.append(category.parent_category.name)
            category = category.parent_category
        else: 
            break
    categories.reverse()
    return categories

@register.filter
def total_price(cart):
    return cart.product.price * cart.quantity

@register.filter
def product_quantity(product, user):
    try: 
        cart = Cart.objects.get(active=True, product=product, user=user).quantity
    except Cart.DoesNotExist:
        return 1
    
    return cart 