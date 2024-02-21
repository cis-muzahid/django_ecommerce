from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product, ProductAttribute, ProductSpecification, Category
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse


# Create your views here.
		
class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'products/index.html', {'products': products})

    def delete(self, request, id):
        print('delete')
        product = Product.objects.get(id=id)
        product.is_delete = True 
        product.save()
        return redirect('product_view_get')
    
    def post(self, request):
        category = Category.objects.get(pk=request.POST.get("category"))

        if category != None:
            products = Product.objects.filter(category=category)


class ProductRetrieve(View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        return render(request, 'products/retrieve.html', {'product': product})        


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", 'description', 'price', 'weight', 'length', 'width', 'height', 'category']
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
	
class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", 'description', 'price', 'weight', 'length', 'width', 'height', 'category']
    template_name_suffix = "_update_form"
    
    def get_success_url(self):
        return reverse('product_view_get')
