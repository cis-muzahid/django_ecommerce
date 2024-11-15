from products.models import Category, Product
from django.core.paginator import Paginator
from .models import Banner

def fetch_all_categories():
    """ function to fetch all parent categories """
    try:
        categories= Category.objects.filter(is_delete=False, parent_category=None)
    except Category.DoesNotExist:
        categories = None
        pass
    return categories

def fetch_category_product(category):
    """ function to fetch all product that belongs to the given category """
    try:
        products = Product.objects.filter(category__in=category, is_delete=False).order_by('-id')
    except Product.DoesNotExist:
        products = None
        pass
    return products

def fetch_categories(category):
    """ fetch all descendants of the given category """
    categories = Category.objects.filter(parent_category=category.id).values_list('id', flat=True)
    subcategory = Category.objects.filter(parent_category__in=categories).values_list('id', flat=True)
    category = Category.objects.filter(id=category.id)
    categories = subcategory.union(categories).union(category)
    return categories

def hot_deals_product():
    """ fetch all products with hot tag """
    return Product.objects.filter(is_delete=False, tag='HOT').order_by('-id')

def pagination(products, page):
    """ function to add paginations on products """
    paginator = Paginator(products, 10)
    page_number = page
    return paginator.get_page(page_number)

def fetch_banner(category):
    """ function to fetch latest wide large banner """
    banner = Banner.objects.filter(category=category.id, type="wide banner large").last()
    try:
        if banner:
            return banner
        else:
            categories = Category.objects.filter(id=category.parent_category.id).values_list('id', flat=True)
            banner = Banner.objects.filter(category__in=categories, type="wide banner large").last()
    except:
        banner = None
    return banner
