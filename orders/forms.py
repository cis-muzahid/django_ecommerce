from typing import Any
from django import forms
from .models import Order, ReturnAndReplaceOrder
from users.models import UserAddress

class OrderForm(forms.ModelForm):
    class Meta:
        """Form for orders"""
        model = Order
        fields = ['total_amount', 'user', 'address', 'status']

class ReturnAndReplaceOrderForm(forms.ModelForm):
    class Meta:
        """Form for orders"""
        model = ReturnAndReplaceOrder
        fields = ['requested', 'order', 'reason', 'action', 'user']

class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['street', 'city', 'state', 'postal_code', 'country']

# class OrderForm(forms.Form):
#     class Meta:
#         """Form for orders"""
#         model = Order
#         fields = ['total_amount', 'user', 'address', 'status','street', 'city', 'state', 'postal_code', 'country']

# class CheckoutForm(forms.Form):
#     street = forms.CharField(max_length=255)
#     city = forms.CharField(max_length=100)
#     state = forms.CharField(max_length=100)
#     postal_code = forms.CharField(max_length=20)
#     country = forms.CharField(max_length=100)
#     payment_method = forms.ChoiceField(choices=[
#         ('stripe', 'Stripe'),
#         ('paypal', 'PayPal'),
#         ('none', 'Checkout Without Payment')
#     ])