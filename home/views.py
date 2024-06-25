from django.shortcuts import render, redirect
from django.views import View
from products.models import Product, Category
from .utilities import *
from .models import Banner, Facility
from blog.models import Blog
from .forms import BannerForm, FacilityForm
from django.contrib import messages

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
            product = Product.objects.get(slug=product)
            category = Category.objects.get(name=category)
            banner =  fetch_banner(category)
            hot_deals = hot_deals.filter(category=category)[:3]
            products = products.filter(category=category)[:5]
            return render(request, 'home/product_details.html', {'categories': categories, 'product': product,
                                                                 'products': products, 'hot_deals':hot_deals,
                                                                 'banner': banner
                                                                 })

        elif category != None:
            """ View for products filtered by category """
            category = Category.objects.get(name=category)
            banner = fetch_banner(category)
            products = fetch_category_product(fetch_categories(category)).order_by('-id')
            products = pagination(products, request.GET.get("page"))
            return render(request, 'home/category.html', {'products': products, 'categories': categories,
                                                          'category': category, 'banner': banner})

        else:
            """ View for Client Home page """
            banners = Banner.objects.filter(active=True).order_by('-id')
            return render(request, 'home.html', {'latest_products': products, 'categories': categories,
                                                 'special_offer_products':products[:3],
                                                 'special_offer_products_2':products[3:6],
                                                 'special_offer_products_3':products[6:9], 'hot_deals': hot_deals[:3],
                                                 'banners': banners.filter(type='header banner'),
                                                 'wide_banner_large': banners.filter(type='wide banner large').first(),
                                                 'wide_banner_small': banners.filter(type='wide banner small').first(),
                                                 'middle_banner': banners.filter(type='middle banner')[:3],
                                                 'blogs': Blog.objects.filter(active=True)[:5]
                                                    } )
        
    def post(self, request, category):
        """ fetch product with price filter """
        category = Category.objects.get(name=category)
        products = fetch_category_product(fetch_categories(category)).order_by('-id')
        products = products.filter(price__range=(request.POST['price'].split(',')))
        return render(request, 'home/category.html', {'products': products, 'categories': fetch_all_categories(),
                                                        'category': category})

class AdminBannerView(View):
    def get(self, request):
        banners = Banner.objects.filter(active=True).order_by('-id')
        categories = Category.objects.filter(is_delete=False)
        return render(request, "admin/home/banner.html", {'banners': banners, 'categories': categories})
    
    def post(self, request):
        banners = Banner.objects.filter(active=True).order_by('-id')
        categories = Category.objects.filter(is_delete=False)
        form = BannerForm(request.POST, request.FILES)
        try: 
            if form.is_valid():
                form.save()
                messages.success(request, "Banner added successfully.")
                return redirect('admin_banner_view')
            else:
                messages.error(request, "An error occurred while adding banner : ", form.errors)
        except Exception as e:
            messages.error(request, "An error occurred while adding banner : ", e)
        
        return render(request, "admin/home/banner.html", {'banners': banners, 'categories': categories})

class AdminBannerUpdateDeleteView(View):
    def get(self, request, pk):
        try:
            categories = Category.objects.filter(is_delete=False)
            banner = Banner.objects.get(id=pk)
            return render(request, "admin/home/edit_banner.html", {'banner': banner})
        except Banner.DoesNotExist as e:
            messages.error(request, "An error occurred while adding banner : ", e)
            return redirect("admin_banner_view")

    def post(self, request, pk):
        categories = Category.objects.filter(is_delete=False)
        banners = Banner.objects.filter(active=True).order_by('-id')
        try:
            banner = Banner.objects.get(id=pk)
        except Banner.DoesNotExist as e:
            messages.error(request, "An error occurred while adding banner : ", e)
            return render(request, "admin/home/banner.html", {'banners': banners, 'categories': categories})
        
        if request.POST.get('action') == "update":
            form = BannerForm(request.POST, request.FILES, instance=banner)
            try: 
                if form.is_valid():
                    form.save()
                    messages.success(request, "Banner updated successfully.")
                    return redirect('admin_banner_view')
                else:
                    messages.error(request, "An error occurred while adding banner : ", form.errors)
            except Exception as e:
                messages.error(request, "An error occurred while adding banner : ", e)
        else: 
            try:
                banner.active = False
                banner.save()
                messages.error(request, "Banner deleted successfully.")
                return redirect('admin_banner_view')
            except Exception as e:
                messages.success(request, "An error occurred while adding banner : ", e)

        return render(request, "admin/home/banner.html", {'banners': banners, 'categories': categories})

class AdminFacilityView(View):
    def get(self, request):
        facilities = Facility.objects.filter(active=True).order_by('-id')
        return render(request, "admin/home/facilities.html", {'facilities': facilities})

    def post(self, request):
        if request.POST.get("facility"):
            action = "updat"
            facility = Facility.objects.get(id=request.POST.get("facility"))
            form = FacilityForm(request.POST, request.FILES, instance=facility)
        else:
            action = "add"
            form = FacilityForm(request.POST, request.FILES)

        facilities = Facility.objects.filter(active=True)
        try: 
            if form.is_valid():
                form.save()
                messages.success(request, f" Facility {action}ed successfully.")
                return redirect('admin_facility_view')
            else:
                messages.error(request, f"An error occurred while {action}ing facility : ", form.errors)
        except Exception as e:
            messages.error(request, f"An error occurred while {action}ing facility : ", e)
        
        return render(request, "admin/home/facilities.html", {'facilities': facilities})

class AdminFacilityDeleteView(View):
    def post(self, request):
        try:
            facility = Facility.objects.get(id=request.POST.get("facility"))
            facility.active = False
            facility.save()
            messages.error(request, f" Facility deleted successfully.")
            return redirect('admin_facility_view')
        except Exception as e:
            facilities = Facility.objects.filter(active=True)
            messages.error(request, "An error occurred while deleting facility : ", e)
            return render(request, "admin/home/facilities.html", {'facilities': facilities})