from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product, ProductAttribute, ProductSpecification, Category
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from .forms import ProductForm
# Create your views here.
		
class ProductView(View):
    def get(self, request, **kargs):
        if kargs and kargs['category'] != None:
            category = Category.objects.get(name=kargs['category'])
            products = Product.objects.filter(category=category)
        else:
            products = Product.objects.all()
        return render(request, 'products/index.html', {'products': products})
class ProductRetrieve(View):
    def get(self, request, id, action):
        if action == 'delete':
            product = Product.objects.get(id=id)
            product.is_delete = True
            product.save()
            return redirect('product_view_get')
        else:
            product = get_object_or_404(Product, id=id)
            return render(request, 'products/retrieve.html', {'product': product})

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('product_view_get')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('product_view_get')

class CreateProductAtrributes(View):
    def get(self, request):
        return render('product_attributes/form.html')

    def post(self, request):
        product = request.POST.get("product_id")
        productattribute = ProductAttribute.objects.create("title", "value", "image")
        productattribute.save()
        return redirect("")

class CreateProductSpecification(View):
    def get(self, request):
        return render('product_attributes/form.html')

    def post(self, request):
        product = request.POST.get("product_id")
        productattribute = ProductSpecification.objects.create("title", "value")
        productattribute.save()
        return redirect("")
