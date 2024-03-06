from typing import Any
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        """Form for orders"""
        model = Order
        fields = ['total_amount', 'user', 'address', 'status']
