from typing import Any
from django import forms
from .models import Order, ReturnAndReplaceOrder

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