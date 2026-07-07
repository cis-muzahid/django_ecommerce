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
        """ Form for user's address """
        model = UserAddress
        fields = ['street', 'city', 'state', 'postal_code', 'country']
