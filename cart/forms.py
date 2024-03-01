from typing import Any
from django import forms
from .models import Cart

class CartForm(forms.ModelForm):
    class Meta:
        """Form for adding product in cart"""
        model = Cart
        fields = ['quantity', 'user', 'product']
