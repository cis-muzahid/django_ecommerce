from typing import List

from django.urls import (path, URLPattern)

from . import views

urlpatterns: List[URLPattern] = [
    path('login_user', views.Login.login_user, name = 'login'),
    path('logout_user', views.Login.logout_user, name = 'logout'),
    path('signup_user', views.Login.signup_user, name='signup'),
    path(route='sub-admin/', view=views.AdminView.as_view(), name='sub-admin'),
]

