from django import template
from orders.models import Order
from users.models import CustomUser
from products.models import Product, Category

register = template.Library()

@register.filter
def orders_count(a):
    """ filter to fetch orders count """
    return Order.objects.count()

@register.filter
def users_count(a):
    """ filter to fetch users count """
    return CustomUser.objects.count()

@register.filter
def products_count(a):
    """ filter to fetch products count """
    return Product.objects.count()

@register.filter
def categories_count(a):
    """ filter to fetch product's categories count """
    return Category.objects.count()
