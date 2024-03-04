from django import template
from django.shortcuts import get_object_or_404
from products.models import ProductAttribute, Product, Category
from cart.models import Cart

register = template.Library()

@register.filter
def subcategories(category):
    try:
        subcategories = Category.objects.filter(parent_category=category)
    except Category.DoesNotExist:
        subcategories = None 
        pass
    return subcategories

@register.filter
def product_attributes(product_id):
    """fetching product attributes"""
    try:
        product_attribute = ProductAttribute.objects.filter(title__icontains='color',product=product_id).first()
    except ProductAttribute.DoesNotExist:
        product_attribute = None
    
    product_attribute = product_attribute.product_image if product_attribute != None else None
    return product_attribute

@register.filter
def product_filter(category):
    categories = Category.objects.filter(parent_category=category).values_list('id', flat=True)
    subcategory = Category.objects.filter(parent_category__in=categories).values_list('id', flat=True)
    products = Product.objects.filter(category__in=subcategory).order_by('-id')
    return products

@register.filter
def electronics_product_filter(category):
    try:
        category = Category.objects.get(name__icontains=category)
    except Category.DoesNotExist:
        category = None 
    category = category.id if category != None else None
    return product_filter(category)

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
def cart_total_price(carts):
    sub_total = 0
    grand_total = 0
    for cart in carts:
        sub_total +=  cart.product.price
        grand_total += cart.product.price * cart.quantity 

    return {'sub_total': sub_total, 'grand_total': grand_total}

@register.filter
def product_quantity(product, user):
    try: 
        cart = Cart.objects.get(active=True, product=product, user=user).quantity
    except Cart.DoesNotExist:
        return 1
    
    return cart 