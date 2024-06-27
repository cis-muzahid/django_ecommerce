from django import forms
from .models import Blog, Comment

class BlogForm(forms.ModelForm):
    class Meta:
        """Form for Blog"""
        model = Blog
        fields = ['title', 'description', 'user', 'image', 'slug']

class CommentForm(forms.ModelForm):
    class Meta:
        """Form for Comment"""
        model = Comment
        fields = ['blog', 'description', 'user', 'parent_comment']