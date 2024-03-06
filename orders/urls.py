# urls.py

from django.urls import path
from .views import OrderView


urlpatterns = [
    path('orders/', OrderView.as_view(), name='orders'),
    path('checkout/', OrderView.as_view(), name='orders'),
]
