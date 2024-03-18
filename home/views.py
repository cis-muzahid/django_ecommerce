from django.shortcuts import render
from django.views import View
from products.models import Product, Category
from .utilities import *

class HomeView(View):
    def get(self, request, category=None, product=None):
        categories = fetch_all_categories()
        hot_deals = hot_deals_product()
        try:
            products = Product.objects.filter(is_delete=False, name__icontains=request.GET['q']).order_by('-id')
            return render(request, 'home/category.html', {'products': products, 'categories': categories })
        except:
            products = Product.objects.filter(is_delete=False).order_by('-id')
        if product !=None:
            """ View for product details """
            product = Product.objects.get(name=product)
            category = Category.objects.get(name=category)
            hot_deals = hot_deals.filter(category=category)[:3]
            products = products.filter(category=category)[:5]
            return render(request, 'home/product_details.html', {'categories': categories, 'product': product,
                                                                 'products': products, 'hot_deals':hot_deals})

        elif category != None:
            """ View for products filtered by category """
            category = Category.objects.get(name=category)
            products = fetch_category_product(fetch_categories(category)).order_by('-id')
            products = pagination(products, request.GET.get("page"))
            return render(request, 'home/category.html', {'products': products, 'categories': categories,
                                                          'category': category})

        else:
            """ View for Client Home page """
            return render(request, 'home.html', {'latest_products': products, 'categories': categories,
                                                 'special_offer_products':products[:3], 'hot_deals': hot_deals[:3] })
        
    def post(self, request, category):
        """ fetch product with price filter """
        category = Category.objects.get(name=category)
        products = fetch_category_product(fetch_categories(category)).order_by('-id')
        products = products.filter(price__range=(request.POST['price'].split(',')))
        return render(request, 'home/category.html', {'products': products, 'categories': fetch_all_categories(),
                                                        'category': category})
        