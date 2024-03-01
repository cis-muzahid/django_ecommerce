from products.models import Category, Product
from django.core.paginator import Paginator

def fetch_all_categories():
    return Category.objects.filter(is_delete=False, parent_category=None)

def fetch_category_product(category):
    return Product.objects.filter(category__in=category, is_delete=False).order_by('-id')

def fetch_categories(category):
    categories = Category.objects.filter(parent_category=category, is_delete=False).values_list('id', flat=True)
    subcategory = Category.objects.filter(parent_category__in=categories, is_delete=False).values_list('id', flat=True)
    category_ids = subcategory or categories or [category.id]
    return category_ids

def hot_deals_product():
    return Product.objects.filter(is_delete=False, tag='HOT').order_by('-id')

def pagination(products, page):
    paginator = Paginator(products, 10)
    page_number = page
    return paginator.get_page(page_number)