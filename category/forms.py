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

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent_category'].queryset = Category.objects.filter(is_delete=False)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if ' ' in name:
            raise forms.ValidationError('Name should not contain spaces.')
        return name
