from cart.models import Cart
from .models import OrderItem
from users.models import CustomUser
from django.conf import settings
from random import randint
import http.client
from datetime import date
import json

def order_cart_item(order, user):
    user = CustomUser.objects.get(id=user)
    carts = Cart.objects.filter(user=user, active=True)
    for cart in carts:
        OrderItem.objects.create(order=order, cart=cart)
        cart.active = False
        cart.save()

def current_user_cart(user):
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
    payload = { "tracking": { "tag": "out_for_delivery" } }
    payload_json = json.dumps(payload)
    conn = http.client.HTTPSConnection("api.aftership.com")
    conn.request("PUT", f"/v4/trackings/fedex/{tracking_number}", payload_json, tracking_header())
    res = conn.getresponse()
    data = res.read()
    data
    pass