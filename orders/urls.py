# urls.py

from django.urls import path
from .views import OrderView

urlpatterns = [
    path('create_order/', OrderView.as_view(), name='create_order'),
    path('orders/', OrderView.as_view(), name='orders'),
]
