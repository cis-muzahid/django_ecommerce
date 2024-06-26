from django.urls import path
from .views import HomeView, AdminBannerView, AdminBannerUpdateDeleteView, AdminFacilityView, AdminFacilityDeleteView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<category>/', HomeView.as_view(), name='categories_product'),
    path('category/<category>/<product>/', HomeView.as_view(), name='product_details'),
    path('admin/banner/', AdminBannerView.as_view(), name='admin_banner_view' ),
    path('admin/banner/<int:pk>/', AdminBannerUpdateDeleteView.as_view(), name='admin_banner_update_delete'),
    path('admin/facilities/', AdminFacilityView.as_view(), name='admin_facilities_view' ),
    path('admin/facilities/delete/', AdminFacilityDeleteView.as_view(), name='admin_facilities_delete'),
]