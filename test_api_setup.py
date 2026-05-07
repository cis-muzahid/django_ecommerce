#!/usr/bin/env python
"""
Test script to verify DRF API setup
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

def test_imports():
    """Test if all our API modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test users app
        from users import serializers as user_serializers
        from users import api_views as user_api_views
        print("✓ Users app imports successful")
        
        # Test products app
        from products import serializers as product_serializers
        from products import api_views as product_api_views
        print("✓ Products app imports successful")
        
        # Test cart app
        from cart import serializers as cart_serializers
        from cart import api_views as cart_api_views
        print("✓ Cart app imports successful")
        
        # Test orders app
        from orders import serializers as order_serializers
        from orders import api_views as order_api_views
        print("✓ Orders app imports successful")
        
        # Test home app
        from home import serializers as home_serializers
        from home import api_views as home_api_views
        print("✓ Home app imports successful")
        
        # Test blog app
        from blog import serializers as blog_serializers
        from blog import api_views as blog_api_views
        print("✓ Blog app imports successful")
        
        # Test category app
        from category import serializers as category_serializers
        from category import api_views as category_api_views
        print("✓ Category app imports successful")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_models():
    """Test if all models are accessible"""
    try:
        print("\nTesting models...")
        
        from users.models import CustomUser, Role, Permission, UserAddress
        from products.models import Category, Product, ProductAttribute, ProductSpecification, ProductReview
        from cart.models import Cart, Wishlist
        from orders.models import Order, OrderItem, ReturnAndReplaceOrder
        from home.models import Banner, Facility
        from blog.models import Blog, BlogCategory, Comment
        
        print("✓ All models accessible")
        return True
        
    except Exception as e:
        print(f"❌ Model error: {e}")
        return False

def test_settings():
    """Test Django settings"""
    try:
        print("\nTesting settings...")
        
        from django.conf import settings
        
        # Check if DRF is in INSTALLED_APPS
        if 'rest_framework' in settings.INSTALLED_APPS:
            print("✓ Django REST Framework installed")
        else:
            print("❌ Django REST Framework not in INSTALLED_APPS")
            return False
        
        # Check if JWT is in INSTALLED_APPS
        if 'rest_framework_simplejwt' in settings.INSTALLED_APPS:
            print("✓ JWT authentication installed")
        else:
            print("❌ JWT authentication not in INSTALLED_APPS")
            return False
        
        # Check REST_FRAMEWORK settings
        if hasattr(settings, 'REST_FRAMEWORK'):
            print("✓ REST_FRAMEWORK settings configured")
        else:
            print("❌ REST_FRAMEWORK settings missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Settings error: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Testing Django DRF API Setup\n")
    
    success = True
    success &= test_settings()
    success &= test_models()
    success &= test_imports()
    
    if success:
        print("\n🎉 All tests passed! DRF API setup is ready.")
        print("\nNext steps:")
        print("1. Run migrations: python manage.py migrate")
        print("2. Create superuser: python manage.py createsuperuser")
        print("3. Start server: python manage.py runserver")
        print("4. Visit API docs: http://localhost:8000/api/docs/")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)