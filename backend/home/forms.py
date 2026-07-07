from django import forms
from .models import Banner, Facility

class BannerForm(forms.ModelForm):
    class Meta:
        """Form for Banners"""
        model = Banner
        fields = ['title', 'subtitle', 'description', 'user', 'image', 'category', 'type']

class FacilityForm(forms.ModelForm):
    """ Form for Facility """
    class Meta:
        model = Facility
        fields = ['title', 'image']