from django.urls import path
from products.views import ProductView, ProductRetrieve, ProductCreateView
from .views import CreateProductSpecification, UpdateProductSpecification, deleteProductAttribute, ProductAttributeView


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [    # products views
    path('products/', ProductView.as_view(), name='product_view_get'),
    path('product/<int:id>/<action>/', ProductRetrieve.as_view(), name='product_retrieve'),
    path('product/', ProductCreateView.as_view(), name='create'),
    path('update_product/<int:pk>/', ProductCreateView.as_view(), name='product_update'),
    path('product/<int:id>/<action>/', ProductRetrieve.as_view(), name='product_delete'),
    path('products/<category>/', ProductView.as_view(), name='filter'),
    path('product/add_specification/<int:product_id>', CreateProductSpecification.as_view(), name='add_product_specification'),
    path('product/<int:product_id>/update_specification/<int:pk>/', UpdateProductSpecification.as_view(), name='update_product_specification'),
    path('delete_product_detail/<int:pk>/<attr>', deleteProductAttribute.as_view(), name='delete_product_specification'),
    path('product_attribute/<int:product_id>/create/', ProductAttributeView.as_view(), name='product_attributes'),
    path('product/<int:product_id>/attribute_update/<int:pk>/', ProductAttributeView.as_view(), name='update_product_attributes'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
