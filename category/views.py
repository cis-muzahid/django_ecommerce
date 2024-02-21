from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from products.models import Category
from django.urls import reverse_lazy


# Create your views here.
class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'

class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'parent_category']
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'parent_category']
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category-list')
    template_name = 'category/category_delete.html'