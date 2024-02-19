from django.urls import path
from products.views import ProductView, ProductRetrieve, ProductCreateView, ProductUpdateView

urlpatterns = [    # products views
    path('products/', ProductView.as_view(), name='product_view_get'),
    path('product/<id>/', ProductRetrieve.as_view(), name='product_retrieve'),
    path('product/', ProductCreateView.as_view(), name='create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    # path('product/<id>/', ProductView.as_view(), name='delete'),
]
