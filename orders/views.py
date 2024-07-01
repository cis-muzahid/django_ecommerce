import stripe
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.shortcuts import redirect
from .models import Order, ReturnAndReplaceOrder
from cart.models import Cart
from .forms import OrderForm, ReturnAndReplaceOrderForm, AddressForm
from django.contrib import messages
from .utilities import *
from home.utilities import *
from datetime import datetime, timedelta
from django.utils import timezone
import paypalrestsdk
from django.views.generic.base import TemplateView
from users.models import UserAddress
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
class OrderView(View):
    def get(self, request):
        """ Orders View for orders list """
        if request.user.id:
            default_address = check_default_address(request.user)
            all_addresses = fetch_user_address(request.user)
            publishable_key = settings.STRIPE_PUBLISHABLE_KEY
            return render(request, 'orders/checkout.html',
                        {'publishable_key': publishable_key, 'default_address': default_address,
                         'all_addresses': all_addresses})
        else:
            return redirect('login_user')

    def post(self, request, pk=None):
        """ Orders View for create orders """
        payment_intent = ''
        if request.POST.get('stripeToken'):
            payment_intent = self.__payment_method(request)
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent)

        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if payment_intent != '' and payment_intent['status'] == 'succeeded':
                order.payment_method = "stripe"
                order.payment_id = payment_intent.id
                order.payment_status = payment_intent['status'] if payment_intent['status'] == 'succeeded' else 'failed'
            # order.tracking_number = create_order_tracking(order)
            order.save()
            order_cart_item(order, request.user.pk)
            messages.success(request,  f'order added successfully.')
            return redirect('home')
        else:
            messages.error(request, form.errors)
            return render(request, 'orders/checkout.html')

    def __payment_method(self, request):
        """ Create strip payment """
        token = request.POST.get('stripeToken')
        source = stripe.Source.create(
                type='card',
                token=token
            )

        customer = None
        for cus in stripe.Customer.list()['data']:
            if cus.email==request.user:
                customer=cus
                break
        if customer == None:
            customer = stripe.Customer.create( email=request.POST.get('stripeEmail'), source=source.id) 
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(float(request.POST['total_amount'])*100),
                currency='inr',
                description='Product payment',
                customer= customer.id,
                source=source,
                setup_future_usage='off_session',
                automatic_payment_methods={ 'enabled': True, 'allow_redirects': 'never' }
            )

            stripe.PaymentIntent.confirm(
                payment_intent.id,
                )

            return payment_intent.id

        except stripe.error.CardError as e:
            error_msg = e.error.message
            return render(request, 'orders/checkout.html')


class UserAddressView(View):
    def get(self, request, pk=None):
        form = AddressForm()
        default_address = check_default_address(request.user)
        all_addresses = fetch_user_address(request.user) 
        return render(request, 'orders/checkout.html', {'form': form, 'default_address': default_address, 'all_addresses': all_addresses })

    def post(self, request, pk=None):
        if request.POST.get('is_default',None) == 'True':
            try:
                UserAddress.objects.filter(user=request.user).update(is_default=False)
            except:
                pass

        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            
            addresses_count = UserAddress.objects.filter(user_id=request.user.id).count()

            if addresses_count == 1 or request.POST.get("is_default", None):
                address.is_default = True
                address.save()
            
            messages.success(request, 'Address added successfully.')
            return redirect(request.META.get('HTTP_REFERER', 'default_url_name'))
        else:
            messages.error(request, 'Something went wrong. Try again.')
            return render(request, 'orders/checkout.html')

class ReturnAndReplaceView(View):
    """ orders list for user """
    def get(self, request):
        order_items = []
        if request.user.id:
            try:
                orders = Order.objects.filter(user=request.user).order_by('-id')
                for order in orders:
                    try:
                        order_items.extend(OrderItem.objects.filter(order=order, active=True, cart__product__name__icontains=request.GET['q']))
                    except:
                        order_items.extend(OrderItem.objects.filter(order=order, active=True))
            except Order.DoesNotExist:
                pass
            return render(request, 'orders/orders.html', {'orders': order_items })
        else:
            return redirect('login_user')

    def post(self, request, pk=None):
        if pk and request.POST.get('requested'):
            """ replace request order item with new order item using cart. """
            replace = ReturnAndReplaceOrder.objects.get(id=pk)
            cart = request.POST.get('cart')
            cart = Cart.objects.get(id=cart)
            replace.cart = cart
            replace.save()
            cart.active = False
            cart.save()
            messages.success(request, 'Your request is completed. Wait sometime for approvment.')
            return redirect('orders_list')

        elif request.POST.get('requested'):
            """ create a request to return or replace order_item """
            carts = current_user_cart(request.user)
            if request.POST.get('action') == 'Replace':
                try:
                    current_time = timezone.now()
                    date_before_seven_days = current_time - timedelta(days=7)
                    replace = ReturnAndReplaceOrder.objects.filter(action='Replace', user=request.user, cart=None, created_at__gte=date_before_seven_days)
                    if replace.exists():
                        messages.success(request,  f'Your previous request is not completed. Please complete or cancel the request.')
                    else:
                        form = ReturnAndReplaceOrderForm(request.POST)
                        if form.is_valid():
                            form.save()
                            messages.success(request,  f'Your request is in progress. Please proceed with products in the cart to complete the request.')
                except Exception as e:
                    messages.info(request, f'An error occurred: {e}')
                return render(request, 'cart/mycart.html', {'carts': carts})

            elif request.POST.get('action') == 'Return':
                form = ReturnAndReplaceOrderForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request,  f'Your request is completed. Wait sometime for approvment.')
                    return redirect('orders_list')

class ChangeOrderStatus(View):
    def post(self, request):
        """ cancle order view for user """
        try:
            order = OrderItem.objects.get(id= request.POST['order'])
        except OrderItem.DoesNotExist:
            order = None

        if order != None:
            order.active = False
            order.save()
            if order.order.payment_status:
                refund = stripe.Refund.create(
                    payment_intent=order.order.payment_status,
                    amount=order.cart.product.price,
                    )
            messages.success(request, 'order is cancelled successfully.')
            return redirect('orders_list')
        else:
            messages.info(request, 'order does not exist.')
            return redirect('orders_list')

class SupplierReturnAndReplaceView(View):
    def get(self, request):
        """ return and replace view for supplier """
        if "return" in request.path:
            orders = ReturnAndReplaceOrder.objects.filter(action='Return', requested=True, approved=False, active=True)
            if request.user.user_role.name =="supplier":
                orders = orders.filter(user = request.user.id)
        else:
            orders = ReturnAndReplaceOrder.objects.filter(action='Replace', requested=True, approved=False, active=True)
            orders = orders.exclude(cart=None)
            if request.user.user_role.name =="supplier":
                orders = orders.filter(user = request.user.id)
        return render(request, 'admin/orders/return_replace.html', {'orders': orders})

    def post(self, request):
        """ return and replace view that allow admin to approve the return and replace request. """
        if request.POST['request']:
            return_replace_request = ReturnAndReplaceOrder.objects.get(id=request.POST['request'])
            return_replace_request.approved = True
            return_replace_request.save()
            if return_replace_request.action == 'Replace':
                return_replace_request.order.cart = return_replace_request.cart
                return_replace_request.order.save()
                return_replace_request.cart = None
                return_replace_request.save()
                return redirect('admin_replace_request_list')
            elif return_replace_request.action == 'Return':
                if return_replace_request.order.order.payment_status:
                    stripe.Refund.create(
                        payment_intent=return_replace_request.order.order.payment_status,
                        amount=return_replace_request.order.cart.product.price,
                        )
                return redirect('admin_return_request_list')

class AdminOrderView(View):
    def get(self, request, pk=None):
        if pk:
            """ order view for admin """
            orders = OrderItem.objects.filter(order=pk)
            if request.user.user_role.name =="supplier":
                orders = orders.filter(user = request.user.id)
            return render(request, 'admin/orders/order_items.html', {'orders': orders})
        else:
            """ order list view for admin """
            orders = Order.objects.all()
            if request.user.user_role.name =="supplier":
                orders = orders.filter(user = request.user.id)
            orders = pagination(orders, request.GET.get("page"))
            return render(request, 'admin/orders/order.html', {'orders': orders})

class CancelRequest(View):
    def post(self, request):
        """ view that allow user to cancle return or replace request. """
        cancel_request = ReturnAndReplaceOrder.objects.get(id=request.POST.get('request'))
        cancel_request.active = False
        cancel_request.save()
        if cancel_request.action == 'return':
            return redirect('admin_return_request_list')
        else:
            return redirect('admin_replace_request_list')


# PAYPAL IMPLEMENTATION===============================================
# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

class CreatePaymentView(View):
    def get(self, request):
        """ payment create view for user """
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal",
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('execute_payment')),
                "cancel_url": request.build_absolute_uri(reverse('payment_failed')),
            },
            "transactions": [
                {
                    "amount": {
                        "total": "10.00",
                        "currency": "USD",
                    },
                    "description": "Payment for Product/Service",
                }
            ],
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
        return render(request, 'payment_failed.html')

class ExecutePaymentView(View):
    def get(self, request):
        """ payment process view for end user """
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            return render(request, 'payment_success.html')
        return render(request, 'payment_failed.html')

class PaymentSuccessView(TemplateView):
    """ paypal payment success view for user """
    template_name = 'payment_success.html'  # Create a template for displaying payment success

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You can add any additional context data here if needed
        return context

class PaymentCheckoutView(View):
    """ paypal payment checkout view """
    def get(self, request):
        return render(request, 'checkout.html')

class PaymentFailedView(View):
    """ paypal payment failed view for user """
    def get(self, request):
        return render(request, 'payment_failed.html')

class OrderTracking(View):
    """ tacking view using order for user """
    def post(self, request):
        order = Order.objects.get(id=request.POST.get('order_id'))
        try:
            orders = OrderItem.objects.filter(order=order, active=True)
        except:
            messages.error(request, 'unable to track this order please try again.')
        return render(request, 'orders/tracking.html', {'orders': orders})
