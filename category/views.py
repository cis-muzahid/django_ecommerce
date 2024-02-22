from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from products.models import Category
from category.forms import CategoryForm
from django.views import View
from django.urls import reverse_lazy


# Create your views here.
class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CategoryDeleteView(View):
    def get(self, request, id):
        category = Category.objects.get(id=id)
        category.is_delete = True 
        category.save()
        return redirect('category-list')