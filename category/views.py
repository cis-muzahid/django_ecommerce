from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView
from products.models import Category
from category.forms import CategoryForm
from django.views import View
from django.urls import reverse_lazy


# Create your views here.
class CategoryListView(View):
    def get(self, request, **kargs):
        if request.GET.get('q'):
            categories = Category.objects.filter(name__icontains=request.GET['q'], is_delete=False)
        else:
            categories = Category.objects.filter(is_delete=False)

        paginator = Paginator(categories, 10)
        page_number = request.GET.get("page")
        categories = paginator.get_page(page_number)
        return render(request, 'category/category_list.html', {'categories': categories})

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
    def get(self, request, pk):
        category = Category.objects.get(id=pk)
        category.is_delete = True 
        category.save()
        return redirect('category-list')