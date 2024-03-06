from django import template
from cart.models import Cart

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