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
            return payment_intent.id
        except stripe.error.CardError as e:
            error_msg = e.error.message
            return render(request, 'orders/checkout.html')
        
class ReturnAndReplaceView(View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        order_items = []
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
        return render(request, 'orders/orders.html', {'orders': order_items })
    
    def post(self, request, pk=None):
        if pk and request.POST.get('requested'):
            replace = ReturnAndReplaceOrder.objects.get(id=pk)
            cart = request.POST.get('cart')
            replace.cart = Cart.objects.get(id=cart)
            replace.save()
            messages.success(request, 'Your request is completed. Wait sometime for approvment.')
            return redirect('orders_list')

        if request.POST.get('requested'):
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
                    # Handle exceptions that may occur during form processing or data saving
                    messages.error(request, f'An error occurred: {e}')
                return render(request, 'cart/mycart.html', {'carts': carts})

            elif request.POST.get('action') == 'Return':
                form = ReturnAndReplaceOrderForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request,  f'Your request is completed. Wait sometime for approvment.')
                    return render(request, 'cart/mycart.html', {'carts': carts } )
