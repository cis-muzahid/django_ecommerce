from django.shortcuts import render, redirect
from products.models import Product, ProductAttribute, ProductSpecification, Category
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from .forms import ProductForm, ProductAttributeForm, ProductSpecificationForm
# Create your views here.

class ProductView(View):
    def get(self, request, **kargs):
        if kargs and kargs['category'] != None:
            category = Category.objects.get(name=kargs['category'])
            products = Product.objects.filter(category=category, is_delete=False)
        else:
            products = Product.objects.filter(is_delete=False)
        return render(request, 'products/index.html', {'products': products})

class ProductRetrieve(View):
    def get(self, request, id, action):
        if action == 'delete':
            product = Product.objects.get(id=id)
            product.is_delete = True
            product.save()
            return redirect('product_view_get')
        else:
            product_specs = ProductSpecification.objects.filter(product=id, is_delete=False)
            return render(request, 'products/retrieve.html', {'product_specs': product_specs, "product_id": id})

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

class CreateProductSpecification(CreateView):
    model = ProductSpecification
    form_class = ProductSpecificationForm
    template_name = 'products/product_spec_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        breakpoint()
        if self.request.POST["save_and_continue"] == 'True':
            return reverse('add_product_specification') + f'?product_id={self.request.POST["product"]}'
        else:
            return reverse('product_retrieve', args=[self.request.POST['product'], 'get'])

    def get_form_kwargs(self):
        kwargs = super(CreateProductSpecification, self).get_form_kwargs()
        kwargs['product'] = self.request.GET.get('product_id')
        return kwargs

class UpdateProductSpecification(UpdateView):
    model = ProductSpecification
    form_class = ProductSpecificationForm
    template_name = 'products/product_spec_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('product_retrieve', args=[self.request.POST['product'], 'get'])
    
class deleteProductAttribute(View):
    def get(self, request, pk, attr):
        if attr == "attributes":
            product_detail = ProductAttribute.objects.get(pk=pk)
        elif attr == "specification":
            product_detail = ProductSpecification.objects.get(pk=pk)

        product_detail.is_delete = True
        product_detail.save()
        return redirect('product_retrieve', product_detail.product.id, 'get')
