from django import template
from django.shortcuts import get_object_or_404
from products.models import ProductAttribute, Product, Category, ProductReview
from cart.models import Cart
from blog.models import Comment
from users.models import Role
from django.db.models import Avg
from django.utils import timezone

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
    category = Category.objects.filter(id=category)
    categories = subcategory.union(categories).union(category)
    products = Product.objects.filter(category__in=categories).order_by('-id')

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
def electronics_sub_categories(category):
    try:
        category = Category.objects.get(name__icontains=category)
        categories = Category.objects.filter(parent_category=category.id)
    except Category.DoesNotExist:
        categories = None
    return categories

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
def product_review(product):
    return ProductReview.objects.filter(product=product)

@register.filter
def product_rating(product):
    average = int(ProductReview.objects.filter(product=product).aggregate(Avg('review'))['review__avg'])
    return average if average else 0

@register.filter
def range_filter(value):
    return range(value)

@register.filter
def product_review_users_count(product):
    return int(ProductReview.objects.filter(product=product).count())

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

@register.filter
def categories_all(a):
    try:
        categories= Category.objects.filter(is_delete=False, parent_category=None)
    except Category.DoesNotExist:
        categories = None
        pass
    return categories

@register.filter
def check_user_role(user):
    try:
        admin_role = Role.objects.get(name="admin")
        user_role = Role.objects.get(name="user")
        if user.user_role == None:
            if user.is_superuser:
                return admin_role.id
            else:
                return user_role.id
    except Role.DoesNotExist:
        return None 
    
@register.filter
def active_header_category(request):
    if 'categor' in request:
        category = Category.objects.get(name = request.split('/')[2])
        if category:
            categories = fetch_all_parent_category(category)
            if categories:
                return categories[0]
            else:
                return category.name
        else:
            return None
    else:
        return None
    
@register.filter
def truncate_description(description):
    return description[:100]

@register.filter
def reply_comments(comment):
    return Comment.objects.filter(active=True, parent_comment=comment)

@register.filter
def comment_time(time):
    now = timezone.now()
    time_difference = now - time
    days = time_difference.days
    if days == 0:
        seconds = time_difference.seconds
        hours = seconds // 3600
        if hours == 0:
            minutes = (seconds % 3600) // 60
            if minutes == 0:
                return f'{ seconds } seconds'
            return f'{ minutes } minutes'
        return f'{ hours } hours'
    return f'{ days } days'

@register.filter
def comments_counts(blog):
    return Comment.objects.filter(active=True, blog=blog).count()
