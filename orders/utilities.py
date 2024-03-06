from cart.models import Cart
from .models import OrderItem
from users.models import CustomUser

def order_cart_item(order, user):
    user = CustomUser.objects.get(id=user)
    carts = Cart.objects.filter(user=user, active=True)
    for cart in carts:
        OrderItem.objects.create(order=order, cart=cart)
        cart.active = False
        cart.save()
