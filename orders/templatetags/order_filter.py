from django import template
from cart.models import Cart
from orders.models import ReturnAndReplaceOrder, OrderItem, Order
from datetime import datetime, timedelta
from django.utils import timezone
from users.models import UserAddress

register = template.Library()

@register.filter
def current_user_cart_total_price(user):
    """ filter to fetch total amount of login user carts """
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
def current_user_cart_total_quantity(user):
    """ filter to fetch total number of carts of login user """
    try:
        total_carts = Cart.objects.filter(user=user, active= True).count()       
        return total_carts
    except Cart.DoesNotExist:
        carts = 0
        return carts

@register.filter
def current_user_replace_request(user):
    """ filter check login user request for return or replace product """
    try:
        current_time = timezone.now()
        date_before_seven_days = current_time - timedelta(days=7)
        replace_orders =  ReturnAndReplaceOrder.objects.filter(action='Replace', user=user, active=True)
        replace_order =  replace_orders.filter(cart=None)
        if replace_order.first() and replace_order.first().order.active and replace_order.first().created_at >= date_before_seven_days and replace_order.first().created_at <= current_time:
            replace_order = replace_order.first().pk
        else:
            replace_order = replace_orders.exclude(cancle_reason=None, approved=True)
            if replace_order.first() and replace_order.first().cancle_reason:
                replace_order = replace_order.first().pk
            else:
                replace_order = None
    except ReturnAndReplaceOrder.DoesNotExist:
        replace_order = None
    return replace_order

@register.filter
def cancle_current_user_replace_request(cart):
    """ filter check login user request for return or replace product is cancled """
    try:
        cart = Cart.objects.get(id=cart)
        replace_order =  ReturnAndReplaceOrder.objects.get(action='Replace', user=cart.user.pk, cart=cart.id, active=True )
        if replace_order:
            replace_order = replace_order.cancle_reason
        else:
            replace_order = None
    except ReturnAndReplaceOrder.DoesNotExist:
        replace_order = None
    return replace_order

@register.filter
def current_user_return_request(order_item):
    """ filter to check login user request is approved or not for return or replace product """
    try:
        replace_order = ReturnAndReplaceOrder.objects.filter(order=order_item).last()
        if replace_order and replace_order.order.active:
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
    """ filter to check login user can create return or replace request or not """
    try:
        order_item = OrderItem.objects.get(id=order_item).order.id
        current_time = timezone.now()
        date_before_seven_days = current_time - timedelta(days=7)
        replace_order = Order.objects.get(id=order_item)
        replace_order = replace_order.created_at >= date_before_seven_days and replace_order.created_at <= current_time
    except Order.DoesNotExist:
        replace_order = False
    return replace_order


@register.filter
def user_address_count(user):
    """ filter to check login user number of addresses """
    try:
        count = UserAddress.objects.filter(user=user).count
    except UserAddress.DoesNotExist:
        count = None
    return count

@register.filter
def check_request_is_cancel(orderid):
    try:
        replace_order = ReturnAndReplaceOrder.objects.get(order=orderid, action="Replace", approved=False)
        if replace_order.cancle_reason:
            return replace_order.cancle_reason
        else:
            return None
    except:
        return None

