from django.shortcuts import render, get_object_or_404
from products.models import Product, ProductAttribute, ProductSpecification
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse


# Create your views here.
		
class ProductView(View):
	def get(self, request):
		products = Product.objects.all()
		return render(request, 'products/index.html', {'products': products})


class ProductRetrieve(View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        return render(request, 'products/retrieve.html', {'product': product})


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", 'description', 'price', 'weight', 'length', 'width', 'height', 'category']
    def get_success_url(self):
        return reverse('product_view_get')
	
class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", 'description', 'price', 'weight', 'length', 'width', 'height', 'category']
    template_name_suffix = "_update_form"
    
    def get_success_url(self):
        return reverse('product_view_get')
