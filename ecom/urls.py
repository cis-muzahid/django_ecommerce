"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    
    path('', include('products.urls')),
    path('', include('home.urls')),
    path('admin/', include('django.contrib.auth.urls')),
    path('', include('users.urls')),
    path('', include('category.urls')),
    path('', include('cart.urls')),
    path('', include('orders.urls')),
    path('', include('blog.urls')),
    
    # API URLs
    path('api/v1/', include('users.api_urls')),
    path('api/v1/', include('products.api_urls')),
    path('api/v1/', include('cart.api_urls')),
    path('api/v1/', include('orders.api_urls')),
    path('api/v1/', include('home.api_urls')),
    path('api/v1/', include('blog.api_urls')),
    path('api/v1/', include('category.api_urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)