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
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
import paypalrestsdk
from django.views.generic.base import TemplateView
from users.models import UserAddress, Vendor
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

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
        payment_intent = None

        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            if request.POST.get('stripeToken'):
                order.payment_method = "stripe"
                stripe_cart_item(order, request.user.pk)
                payment_intent = self.__payment_method_stripe(request)
                order.payment_id = payment_intent
                order.save()
            if payment_intent == None:
                order.payment_method = "cash on delivery"
                order_cart_item(order, request.user.pk)
                order.save()
            return redirect('home')
        else:
            messages.error(request, form.errors)
            return render(request, 'orders/checkout.html')

    def __payment_method_stripe(self, request):
        """ Create strip payment """
        try:
            token = request.POST.get('stripeToken')
            email = request.POST.get('stripeEmail')
            total_amount = int(float(request.POST['total_amount']) * 100)
            address = request.POST.get('address')
            source = stripe.Source.create(
                type='card',
                token=token
            )

            customer = None
            for cus in stripe.Customer.list(email=email)['data']:
                if cus.email == email:
                    customer = cus
                    break
            if customer is None:
                customer = stripe.Customer.create(
                    email=email,
                    source=source.id,
                    address=retrive_address(address)
                )

            else:
                stripe.Customer.modify(
                    customer['id'],
                    name=request.user.first_name,
                    address=retrive_address(address)
                )
                stripe.Customer.create_source(
                    customer.id,
                    source=source.id
                )

            # Create a PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=total_amount,
                currency='inr',
                description='Product payment',
                customer=customer.id,
                payment_method=source.id,
                setup_future_usage='off_session',
                automatic_payment_methods={'enabled': True, 'allow_redirects': 'never'}
            )

            stripe.PaymentIntent.confirm(
                payment_intent.id,
                payment_method=source.id
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
            if replace.cancle_reason:
                replace.active = True
                replace.approved = False
            replace.save()
            cart.active = False
            cart.save()
            messages.success(request, 'Your return request is completed. Please wait for some time to be approved by the admin.')
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
            if order.order.payment_method=='stripe':
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
            orders = ReturnAndReplaceOrder.objects.filter(action='Return' )
            if request.user.user_role and request.user.user_role.name =="supplier":
                orders = orders.filter(user = request.user.id)
        else:
            orders = ReturnAndReplaceOrder.objects.filter(action='Replace')
            orders = orders.exclude(cart=None)
            if request.user.user_role and request.user.user_role.name =="supplier":
                orders = orders.filter(user = request.user.id)
        orders = orders.filter(requested=True, approved=False, active=True)
        return render(request, 'admin/orders/return_replace.html', {'orders': orders})

    def post(self, request):
        """ return and replace view that allow admin to approve the return and replace request. """
        if request.POST['request']:
            return_replace_request = ReturnAndReplaceOrder.objects.get(id=request.POST['request'])
            return_replace_request.approved = True
            return_replace_request.save()
            if return_replace_request.action == 'Replace':
                amount = (return_replace_request.order.cart.product.price - return_replace_request.cart.product.price)
                return_replace_request.order.cart = return_replace_request.cart
                return_replace_request.order.save()
                return_replace_request.active = False
                return_replace_request.save()
                if return_replace_request.order.order.payment_method == 'stripe':
                    # stripe.Refund.create(
                    #    payment_intent=return_replace_request.order.order.payment_id,
                    #    amount=int(float(amount)*100)
                    # )
                    pass
                return redirect('admin_replace_request_list')
            elif return_replace_request.action == 'Return':
                if return_replace_request.order.order.payment_method == 'stripe':
                    return_replace_request.active = False
                    return_replace_request.save()
                    stripe.Refund.create( 
                       payment_intent=return_replace_request.order.order.payment_id, 
                       amount=int(float(return_replace_request.order.cart.product.price)*100)
                    )
                return redirect('admin_return_request_list')

class AdminOrderView(View):
    def get(self, request, pk=None):
        if pk:
            """ order view for admin """
            orders = OrderItem.objects.filter(order=pk)
            if request.user.user_role and request.user.user_role.name =="supplier":
                orders = orders.filter(user = request.user.id, active=True)
            return render(request, 'admin/orders/order_items.html', {'orders': orders})
        else:
            """ order list view for admin """
            orders = Order.objects.all()
            if request.user.user_role and request.user.user_role.name =="supplier":
                orders = orders.filter(user = request.user.id, active=True)
            orders = pagination(orders, request.GET.get("page"))
            return render(request, 'admin/orders/order.html', {'orders': orders})

class AdminDeleteOrder(View):
    def post(self, request):
        try:
            order = Order.objects.get(id=request.POST.get('order'))
            order.active = False
            order.save()
        except:
            messages.error(request, 'Something went wrong. Try again.')
        return redirect('admin_orders_list')

class CancelRequest(View):
    def post(self, request):
        """ view that allow user to cancle return or replace request. """
        cancel_request = ReturnAndReplaceOrder.objects.get(id=request.POST.get('request'))
        if cancel_request.action == 'Return':
            cancel_request.active = False
        else:
            cancel_request.cart.active = True
            cancel_request.cart.save()
            cancel_request.active = False
            cancel_request.cancle_reason = "Admin reject this replace request."
        cancel_request.save()
        if cancel_request.action == 'Return':
            return redirect('admin_return_request_list')
        else:
            return redirect('admin_replace_request_list')


# PAYPAL IMPLEMENTATION===============================================
# Configure PayPal SDK

class CreatePaymentView(View):
    template_name = 'payment.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Payment creation handled on client side, so no need to handle here.
        return render(request, self.template_name)


class ExecutePaymentView(View):
    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id = request.user.pk)
            order = Order.objects.create(user=user, total_amount=request.GET.get('total_amount'),
                                        address = request.GET.get('address'))
            order.payment_id = request.GET.get('paymentId')
            order.payment_method = 'paypal'
            order.payment_status = 'succeeded'
            order.save()
            order_cart_item(order, request.user.pk)
        except Exception as e:
            messages.error(request, 'Facing an issue while creating a order : ', e)
        return redirect('home')


class PaymentCancelledView(View):
    def get(self, request, *args, **kwargs):
        messages.error(request, 'Something went wrong. Try again.')
        return redirect('cart_view')

class OrderTracking(View):
    """ tacking view using order for user """
    def post(self, request):
        order = Order.objects.get(id=request.POST.get('order_id'))
        try:
            orders = OrderItem.objects.filter(order=order, active=True)
        except:
            messages.error(request, 'unable to track this order please try again.')
        return render(request, 'orders/tracking.html', {'orders': orders})

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_WEBHOOK_KEY

        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return HttpResponse(status=400)

        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            self.handle_payment_intent_succeeded(payment_intent)
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            self.handle_payment_intent_failed(payment_intent)
        else:
            # Unexpected event type
            return HttpResponse(status=400)
        return HttpResponse(status=200)

    def handle_payment_intent_succeeded(self, payment_intent):
        order = Order.objects.filter(payment_id=payment_intent.id).first()
        order.payment_status = 'succeeded'
        order.save()
        create_order_item(order)
        process_payment(order)

    def handle_payment_intent_failed(self, payment_intent):
        try:
            order = Order.objects.filter(payment_id=payment_intent.id).first()
            order.payment_status = 'failed'
            order.save()
        except:
            pass
