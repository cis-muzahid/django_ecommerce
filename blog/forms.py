from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        """Form for Banners"""
        model = Blog
        fields = ['title', 'description', 'user', 'image', 'slug']