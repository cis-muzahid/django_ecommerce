from django.urls import path
from .views import LoginView, LogoutView, SignupView, UserIndexView, AddUserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('user/index/', UserIndexView.as_view(), name='user_index'),
    path('user/add/', AddUserView.as_view(), name='add_user'),
    # Add more paths as needed for your application
]
