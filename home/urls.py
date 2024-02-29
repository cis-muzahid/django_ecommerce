from django.urls import path
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<category>/', HomeView.as_view(), name='category'),
    path('<category>/<product>/', HomeView.as_view(), name='category')
]