from django import forms
from products.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        """ Form for Category """
        model = Category
        fields = ['name', 'parent_category', 'user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_category': forms.Select(attrs={'class': 'custom-select form-control'})
        }