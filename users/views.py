from django.shortcuts import render
from django.views import generic



class HomeView(generic.TemplateView):
    template_name: str = 'home.html'


class AdminView(generic.TemplateView):
    template_name: str = 'admin/home.html'
