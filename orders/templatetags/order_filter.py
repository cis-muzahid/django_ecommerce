from django import template
from cart.models import Cart
from orders.models import ReturnAndReplaceOrder

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
    # breakpoint()
    try: 
        replace_order = ReturnAndReplaceOrder.objects.get(user=user, cart=None).id
    except ReturnAndReplaceOrder.DoesNotExist:
        replace_order = None
    return replace_order