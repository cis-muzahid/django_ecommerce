from cart.models import Cart
from .models import OrderItem, CartOrderItem
from users.models import CustomUser, UserAddress, Vendor
from django.conf import settings
from random import randint
import http.client
from datetime import date
import json
import time
import paypalrestsdk

paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

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
        if not CartOrderItem.objects.filter(order=order, cart=cart).exists():
            OrderItem.objects.create(order=order, cart=cart)
            cart.active = False
            cart.save()

def stripe_cart_item(order, user):
    """ function to create cart order items when user choose stripe for payment """
    user = CustomUser.objects.get(id=user)
    carts = Cart.objects.filter(user=user, active=True)
    for cart in carts:
        if not CartOrderItem.objects.filter(order=order, cart=cart).exists():
            CartOrderItem.objects.create(order=order, cart=cart).save()


def create_order_item(order):
    """ function to create order items after successful payment from stripe """
    carts = CartOrderItem.objects.filter(order=order, active=True)
    for cart in carts:
        if not OrderItem.objects.filter(order=order, cart=cart.cart).exists():
            OrderItem.objects.create(order=order, cart=cart.cart)
        cart.active = cart.cart.active = False
        cart.save()
        cart.cart.save()

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

def process_payment(self, order):
    order_items = OrderItem.objects.filter(order=order)
    for order_item in order_items:
        vendor = order_item.cart.product.user
        vendor_user = Vendor.objects.filter(user=vendor).first()
        # send_payment_to_vendor(order_item.cart.product.price, vendor.email)
        if not vendor_user:
            vendor = Vendor.objects.create(user=vendor)
            vendor.account_balance = order_item.cart.product.price
            vendor.save()
        else:
            vendor_user.account_balance += order_item.cart.product.price
            vendor_user.save()

def send_payment_to_vendor(self, amount, email):
    try:
        payout = paypalrestsdk.Payout({
            "sender_batch_header": {
                "sender_batch_id": "batch_" + str(int(time.time())),
                "email_subject": "You have a payment"
            },
            "items": [{
                "recipient_type": "EMAIL",
                "amount": {
                    "value": int(float(amount)*100),
                    "currency": "USD"
                },
                "receiver": email,
                "note": "Thank you.",
                "sender_item_id": "item_1"
            }]
        })
        
        if payout.create(sync_mode=True):
            print("Payout created successfully")
            return payout
        else:
            print("Failed to create payout")
            print(payout.error)
            return None

    except paypalrestsdk.ResourceNotFound as error:
        print("ResourceNotFound Error: ", error)
    except Exception as e:
        print("An error occurred: ", str(e))
