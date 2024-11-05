from django import forms
from .models import Blog, Comment, BlogCategory
    
class BlogCategoryForm(forms.ModelForm):
    class Meta:
        """ Form for Blog Category """
        model = BlogCategory
        fields = ['name', 'user']

class BlogForm(forms.ModelForm):
    class Meta:
        """Form for Blog"""
        model = Blog
        fields = ['title', 'description', 'user', 'image', 'slug', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        """Form for Comment"""
        model = Comment
        fields = ['blog', 'description', 'user', 'parent_comment']