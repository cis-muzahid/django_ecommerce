# urls.py

from django.urls import path
from .views import OrderView, ReturnAndReplaceView


urlpatterns = [
    path('orders/', ReturnAndReplaceView.as_view(), name='orders_list'),
    path('checkout/', OrderView.as_view(), name='orders'),
    path('orders/replace/<pk>', ReturnAndReplaceView.as_view(), name='replace_product'),
]
