from django import template
from orders.models import Order
from users.models import CustomUser
from products.models import Product, Category

register = template.Library()

@register.filter
def orders_count(a):
    return Order.objects.count()

@register.filter
def users_count(a):
    return CustomUser.objects.count()

@register.filter
def products_count(a):
    return Product.objects.count()

@register.filter
def categories_count(a):
    return Category.objects.count()
