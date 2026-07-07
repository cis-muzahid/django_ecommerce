from typing import Any
from django import forms
from .models import Cart, Wishlist

class CartForm(forms.ModelForm):
    quantity = forms.IntegerField(required=False)
    class Meta:
        """Form for adding product in cart"""
        model = Cart
        fields = ['quantity', 'user', 'product']

        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }


class WishlistForm(forms.ModelForm):
    class Meta:
        """ Form for adding products in wishlists"""
        model = Wishlist
        fields = ['user', 'product']