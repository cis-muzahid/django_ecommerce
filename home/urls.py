from django.urls import path
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<category>/', HomeView.as_view(), name='categories_product'),
    path('category/<category>/<product>/', HomeView.as_view(), name='product_details')
]