import stripe
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.shortcuts import redirect
from .models import Order, ReturnAndReplaceOrder
from cart.models import Cart
from .forms import OrderForm, ReturnAndReplaceOrderForm
from django.contrib import messages
from .utilities import *
from home.utilities import *
from datetime import datetime, timedelta
from django.utils import timezone
from home.utilities import *

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
class OrderView(View):
    def get(self, request):
        """ Orders View for orders list """
        publishable_key = settings.STRIPE_PUBLISHABLE_KEY
        return render(request, 'orders/checkout.html', {'publishable_key': publishable_key})

    def post(self, request, pk=None):
        """ Orders View for create orders """
        payment_intent = ''
        if request.POST.get('stripeToken'):
            payment_intent = self.__payment_method(request)
        form = OrderForm(request.POST)
        if form.is_valid():    
            order = form.save(commit=False)
            order.payment_status = payment_intent 
            order.tracking_number = create_order_tracking(order)
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
                setup_future_usage='off_session' 
            )

            stripe.PaymentIntent.confirm(
                payment_intent.id,
                payment_method="pm_card_visa",
                )

            if payment_intent.status == 'successful':
                return payment_intent.id
            else:
                messages.error(request, 'Payment is not completed by this method. please try again.')
                return render(request, 'orders/checkout.html')

        except stripe.error.CardError as e:
            error_msg = e.error.message
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
        if "return" in request.path:
            orders = ReturnAndReplaceOrder.objects.filter(action='Return', requested=True, approved=False, active=True)
        else:
            orders = ReturnAndReplaceOrder.objects.filter(action='Replace', requested=True, approved=False, active=True)
            orders = orders.exclude(cart=None)
        return render(request, 'admin/orders/return_replace.html', {'orders': orders})

    def post(self, request):
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
            orders = OrderItem.objects.filter(order=pk)
            return render(request, 'admin/orders/order_items.html', {'orders': orders})
        else:
            orders = Order.objects.all()
            orders = pagination(orders, request.GET.get("page"))
            return render(request, 'admin/orders/order.html', {'orders': orders})

class CancelRequest(View):
    def post(self, request):
        cancel_request = ReturnAndReplaceOrder.objects.get(id=request.POST.get('request'))
        cancel_request.active = False
        cancel_request.save()
        if cancel_request.action == 'return':
            return redirect('admin_return_request_list')
        else:
            return redirect('admin_replace_request_list')

class OrderTracking(View):
    def post(self, request):
        order = Order.objects.get(id=request.POST.get('order_id'))
        try:
            orders = OrderItem.objects.filter(order=order, active=True)
        except:
            messages.error(request, 'unable to track this order please try again.')
        return render(request, 'orders/tracking.html', {'orders': orders})
