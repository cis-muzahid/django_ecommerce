from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from products.models import Product, ProductAttribute, ProductSpecification, Category
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from .forms import ProductForm, ProductAttributeForm, ProductSpecificationForm
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.

class ProductView(View):
    def get(self, request, **kargs):
        if request.user.is_authenticated:
            if kargs and kargs['category'] != None:
                category = Category.objects.get(name=kargs['category'])
                products = Product.objects.filter(category=category, is_delete=False)
            elif request.GET.get('q'):
                products = Product.objects.filter(name__icontains=request.GET['q'], is_delete=False)
            else:
                products = Product.objects.filter(is_delete=False)
            
            paginator = Paginator(products, 10)
            page_number = request.GET.get("page")
            products = paginator.get_page(page_number)
            return render(request, 'admin/products/index.html', {'products': products})
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('admin_login')

class ProductRetrieve(View):
    def get(self, request, id, action):
        if action == 'delete':
            product = Product.objects.get(id=id)
            product.is_delete = True
            product.save()
            return redirect('product_view_get')
        else:
            product_specs = ProductSpecification.objects.filter(product=id, is_delete=False)
            product_attr = ProductAttribute.objects.filter(product=id, is_delete=False)
            product = get_object_or_404(Product, pk=id)
            return render(request, 'admin/products/retrieve.html', {'product_specs': product_specs,'product_attr': product_attr, "product": product})

class ProductCreateView(CreateView, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin/products/product_form.html'
    
    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return get_object_or_404(Product, pk=self.kwargs['pk'])
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):      
        if self.kwargs:
            return reverse('product_view_get')
        else: 
            return reverse('product_attributes', kwargs={'product_id': self.object.pk})

class CreateProductSpecification(CreateView):
    form_class = ProductSpecificationForm
    template_name = 'admin/products/product_spec_form.html'

    def get(self, request, product_id):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'product_id': product_id})

    def post(self, request, product_id):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save(commit=False)
                product.product_id = product_id
                product.save()
                if self.request.POST.get("save_and_continue") == 'True':
                    return HttpResponseRedirect(request.path_info)  
                else:
                    product_specs = ProductSpecification.objects.filter(product=product_id, is_delete=False)
                    product_attr = ProductAttribute.objects.filter(product=product_id, is_delete=False)
                    product = get_object_or_404(Product, pk=product_id)
                    return render(request, 'admin/products/retrieve.html', {'product_specs': product_specs,'product_attr': product_attr, "product": product})
            except Exception as e:
                print("Error:", e)
                error_message = "An error occurred while saving the product attribute."
                return render(request, self.template_name, {'form': form, 'product_id': product_id, 'error_message': error_message})
        else:
            return render(request, self.template_name, {'form': form, 'product_id': product_id})


class UpdateProductSpecification(UpdateView):
    model = ProductSpecification
    form_class = ProductSpecificationForm
    template_name = 'admin/products/product_spec_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('product_retrieve', args=[self.kwargs['product_id'], 'get'])
    
class deleteProductAttribute(View):
    def get(self, request, pk, attr):
        if attr == "attributes":
            product_detail = ProductAttribute.objects.get(pk=pk)
        elif attr == "specification":
            product_detail = ProductSpecification.objects.get(pk=pk)

        product_detail.is_delete = True
        product_detail.save()
        return redirect('product_retrieve', product_detail.product.id, 'get')

class ProductAttributeView(View):
    form_class = ProductAttributeForm
    template_name = 'admin/products/product_spec_form.html'

    def get(self, request, product_id, pk=None):
        if pk:
            product_attribute = get_object_or_404(ProductAttribute, pk=pk)
            form = self.form_class(instance=product_attribute)
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form, 'product_id': product_id})

    def post(self, request, product_id, pk=None):
        if pk:
            product_attribute = get_object_or_404(ProductAttribute, pk=pk)
            form = self.form_class(request.POST, request.FILES, instance=product_attribute)
        else:
            form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save(commit=False)
                product.product_id = product_id
                product.save()
                if self.request.POST.get("save_and_continue") == 'True':
                    return HttpResponseRedirect(request.path_info)  
                else:
                    if pk:
                        product_specs = ProductSpecification.objects.filter(product=product_id, is_delete=False)
                        product_attr = ProductAttribute.objects.filter(product=product_id, is_delete=False)
                        product = get_object_or_404(Product, pk=product_id)
                        return render(request, 'admin/products/retrieve.html', {'product_specs': product_specs,'product_attr': product_attr, "product": product})
                    else:
                        return redirect(reverse('add_product_specification', kwargs={'product_id': product_id}))
            except Exception as e:
                print("Error:", e)
                error_message = "An error occurred while saving the product attribute."
                return render(request, self.template_name, {'form': form, 'product_id': product_id, 'error_message': error_message})
        else:
            return render(request, self.template_name, {'form': form, 'product_id': product_id})


