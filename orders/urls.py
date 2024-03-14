# urls.py

from django.urls import path
from .views import OrderView, ReturnAndReplaceView, ChangeOrderStatus, AdminOrderView, SupplierReturnAndReplaceView


urlpatterns = [
    path('orders/', ReturnAndReplaceView.as_view(), name='orders_list'),
    path('checkout/', OrderView.as_view(), name='orders'),
    path('orders/replace/<pk>/', ReturnAndReplaceView.as_view(), name='replace_product'),
    path('order/cancel/', ChangeOrderStatus.as_view(), name='order_status'),
    path('admin_orders/', AdminOrderView.as_view(), name='admin_orders_list'),
    path('admin_orders/<pk>', AdminOrderView.as_view(), name='admin_orders_item_list'),
    path('replace_order/', SupplierReturnAndReplaceView.as_view(), name='admin_replace_request_list'),
    path('return_order/', SupplierReturnAndReplaceView.as_view(), name='admin_return_request_list'),
]
