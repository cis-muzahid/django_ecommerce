from django import template
from cart.models import Cart
from orders.models import ReturnAndReplaceOrder, OrderItem, Order
from datetime import datetime, timedelta
from django.utils import timezone


register = template.Library()

@register.filter
def current_user_cart_total_price(user):
    try:
        carts = Cart.objects.filter(user=user, active= True)
        grand_total = 0
        for cart in carts:
            grand_total += cart.product.price * cart.quantity
        return grand_total
    except Cart.DoesNotExist:
        carts = None
        return carts

@register.filter
def current_user_replace_request(user):
    try:
        current_time = timezone.now()
        date_before_seven_days = current_time - timedelta(days=7)
        replace_order =  ReturnAndReplaceOrder.objects.get(action='Replace', user=user, cart=None)
        if replace_order.created_at >= date_before_seven_days and replace_order.created_at <= current_time:
            replace_order = replace_order.id
        else:
            replace_order = None
    except ReturnAndReplaceOrder.DoesNotExist:
        replace_order = None
    return replace_order

@register.filter
def current_user_return_request(order_item):
    try:
        replace_order = ReturnAndReplaceOrder.objects.get(order=order_item)
        if replace_order.approved and replace_order.action == 'Return':
            replace_order = 'Approved'
        elif replace_order.approved and replace_order.action == 'Replace':
            replace_order = None
        else:
            replace_order = replace_order.action
    except ReturnAndReplaceOrder.DoesNotExist:
        replace_order = None
    return replace_order

@register.filter
def is_last_seven_days_order(order_item):
    try:
        order_item = OrderItem.objects.get(id=order_item).order.id
        current_time = timezone.now()
        date_before_seven_days = current_time - timedelta(days=7)
        replace_order = Order.objects.get(id=order_item)
        replace_order = replace_order.created_at >= date_before_seven_days and replace_order.created_at <= current_time
    except Order.DoesNotExist:
        replace_order = False
    return replace_order