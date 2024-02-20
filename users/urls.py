from typing import List

from django.urls import (path, URLPattern)

from . import views

urlpatterns: List[URLPattern] = [
    path(route='', view=views.HomeView.as_view(), name='user'),
    path(route='sub-admin/', view=views.AdminView.as_view(), name='sub-admin'),
]

