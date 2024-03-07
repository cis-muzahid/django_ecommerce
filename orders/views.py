import stripe
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.shortcuts import redirect
from .models import Order
from cart.models import Cart
from .forms import OrderForm
from django.contrib import messages
from .utilities import *
from datetime import timezone, timedelta
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
    
    def post(self, request):
        return redirect('orders_list')