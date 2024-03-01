from django.urls import path
from .views import CartView, WishlistView, DeleteView

urlpatterns = [  
    path('my_cart/', CartView.as_view(), name='cart_view'),
    path('add_cart/', CartView.as_view(), name='add_cart_view'),
    path('update_cart/', CartView.as_view(), name='update_cart_view'),
    path('my_wishlist/', WishlistView.as_view(), name='wishlist_view'),
    path('add_to_wishlist/', WishlistView.as_view(), name='add_wishlist_view'),
    path('remove_product/<action>/<pk>/', DeleteView.as_view(), name='delete_cart_product')
]