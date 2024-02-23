from django.urls import path
from products.views import ProductView, ProductRetrieve, ProductCreateView, ProductUpdateView
from .views import CreateProductSpecification, UpdateProductSpecification, deleteProductAttribute

urlpatterns = [    # products views
    path('products/', ProductView.as_view(), name='product_view_get'),
    path('product/<int:id>/<action>/', ProductRetrieve.as_view(), name='product_retrieve'),
    path('product/', ProductCreateView.as_view(), name='create'),
    path('update_product/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:id>/<action>/', ProductRetrieve.as_view(), name='product_delete'),
    path('products/<category>/', ProductView.as_view(), name='filter'),
    path('product/add_specification/', CreateProductSpecification.as_view(), name='add_product_specification'),
    path('product/update_specification/<int:pk>/', UpdateProductSpecification.as_view(), name='update_product_specification'),
    path('delete_product_detail/<int:pk>/<attr>', deleteProductAttribute.as_view(), name='delete_product_specification'),

]
