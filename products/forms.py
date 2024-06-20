from typing import Any
from django import forms
from .models import Product, ProductAttribute, ProductSpecification, ProductReview

class ProductForm(forms.ModelForm):
    class Meta:
        """Form for product"""
        model = Product
        fields = ['name', 'description', 'price', 'weight', 'length', 'width', 'height', 'category', 'user', 'tag']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'width': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'custom-select form-control'}),
            'tag': forms.Select(attrs={'class': 'custom-select form-control'},
                                choices=[('', 'None'), ('SALE', 'Sale'), ('NEW', 'New'), ('HOT', 'Hot')]),
        }


class ProductAttributeForm(forms.ModelForm):
    class Meta:
        """Form for product attributes"""
        model = ProductAttribute
        fields = ['title', 'value', 'product_image', 'out_of_stoke', 'is_display', 'product']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ImageField(),
            'out_of_stoke': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_display': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def __init__(self, *args, **kwargs):
        """Init method for overriding fields objects."""
        product = kwargs.pop('product', None)
        super(ProductAttributeForm, self).__init__(*args, **kwargs)
        
        self.fields['product'].initial = product
        self.fields['product'].widget = forms.HiddenInput()

class ProductSpecificationForm(forms.ModelForm):
    class Meta:
        """Form for product specification"""
        model = ProductSpecification
        fields = ['title', 'description', 'product']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            }

    def __init__(self, *args, **kwargs):
        """Init method for overriding fields objects."""
        product = kwargs.pop('product', None)
        super(ProductSpecificationForm, self).__init__(*args, **kwargs)
        
        self.fields['product'].initial = product
        self.fields['product'].widget = forms.HiddenInput()


class ProductReviewForm(forms.ModelForm):
    class Meta:
        """Form for user review"""
        model = ProductReview
        fields = ['review', 'title', 'comment', 'user', 'product']
