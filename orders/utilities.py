from cart.models import Cart
from .models import Order, OrderItem
from users.models import CustomUser, UserAddress

ONLINE_PAYMENT_METHODS = ('razorpay', 'paypal')
PAID_PAYMENT_STATUSES = ('succeeded', 'authorized', 'processing')


def finalize_order_carts(order):
    """Mark cart items as purchased after successful payment."""
    if not order.active:
        order.active = True
        order.save(update_fields=['active', 'updated_at'])

    for order_item in OrderItem.objects.filter(order=order, active=True).select_related('cart'):
        cart = order_item.cart
        if cart.active:
            cart.active = False
            cart.save(update_fields=['active'])


def cancel_unpaid_order(order):
    """Cancel a failed/abandoned checkout without removing items from the user's cart."""
    if order.payment_status in PAID_PAYMENT_STATUSES:
        return False

    order.status = 'cancelled'
    order.payment_status = 'failed'
    order.active = False
    order.save(update_fields=['status', 'payment_status', 'active', 'updated_at'])
    OrderItem.objects.filter(order=order).update(active=False)
    return True


def cancel_stale_pending_orders(user):
    """Cancel older unpaid online-payment orders before starting a new checkout."""
    pending_orders = Order.objects.filter(
        user=user,
        payment_method__in=ONLINE_PAYMENT_METHODS,
        status__in=['initial', 'in_process'],
    ).exclude(payment_status__in=PAID_PAYMENT_STATUSES)

    for order in pending_orders:
        cancel_unpaid_order(order)
from django.conf import settings
from random import randint
import http.client
from datetime import date
import json

def check_default_address(user):
    """ function to check login user default address """
    try:
        return UserAddress.objects.get(user_id=user.id, is_default=True)
    except UserAddress.DoesNotExist:
        return None

def order_cart_item(order, user):
    """ function to create order items when user create order """
    user = CustomUser.objects.get(id=user)
    carts = Cart.objects.filter(user=user, active=True)
    for cart in carts:
        OrderItem.objects.create(order=order, cart=cart)
        cart.active = False
        cart.save()

def current_user_cart(user):
    """ function to fetch all carts of login user """
    try:
        carts =  Cart.objects.filter(user=user.id, active=True)
    except Cart.DoesNotExist:
        carts = None
    return carts

Tracking_key = settings.TRACKING_KEY

def tracking_header():
    headers = {
        'Content-Type': "application/json",
        'as-api-key': Tracking_key
        }
    return headers

def create_order_tracking(order):
    """ function to create order tracking """
    tracking_number = randint(1000, 10000)
    order_id = order.id
    conn = http.client.HTTPSConnection("api.aftership.com")
    payload_template = """{ "tracking": { "slug": "fedex",
                                 "tracking_number": "%s",
                                 "title": "tracking",
                                 "smses": [ "+18555072509", "+18555072501" ],
                                 "emails": [ "%s" ],
                                 "order_id": "%s",
                                 "order_number": "%s",
                                 "order_id_path": "http://www.aftership.com/order_id=%s",
                                 "custom_fields": { "product_name": "iPhone Case", "product_price": "USD19.99" },
                                 "language": "en",
                                 "order_promised_delivery_date": "%s",
                                 "delivery_type": "pickup_at_store",
                                 "pickup_location": "Flagship Store",
                                 "pickup_note": "Reach out to our staffs when you arrive our stores for shipment pickup",
                                 "origin_country_iso3": "IND",
                                 "origin_state": "Madhya Pradesh",
                                 "origin_city": "Indore",
                                 "origin_postal_code": "452010",
                                 "origin_raw_location": "Lihong Gardon 4A 2301, Chaoyang District, Indore, <P, 452010, India",
                                 "destination_country_iso3": "IND",
                                 "destination_state": "madhya pradesh",
                                 "destination_city": "indore",
                                 "destination_postal_code": "452010",
                                 "destination_raw_location": "13th Street, Indore, MP, 452010, IN, India" } }"""

    today_date = date.today().isoformat() 
    payload = payload_template % (tracking_number, order.user.email, order_id, order_id, order_id, today_date)
    conn.request("POST", "/tracking/2024-04/trackings", payload, tracking_header())
    res = conn.getresponse()
    data = res.read()
    return tracking_number

def update_tracking_status(tracking_number):
    """ function to update tracking status """
    payload = { "tracking": { "tag": "out_for_delivery" } }
    payload_json = json.dumps(payload)
    conn = http.client.HTTPSConnection("api.aftership.com")
    conn.request("PUT", f"/v4/trackings/fedex/{tracking_number}", payload_json, tracking_header())
    res = conn.getresponse()
    data = res.read()
    data
    pass

def fetch_user_address(user):
    """ function to fetch all login user's address """
    try:
        addresses = UserAddress.objects.filter(user=user)
    except:
        addresses = None
    return addresses