from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .api_views import (
    UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView,
    ChangePasswordView, PasswordResetView, PasswordResetConfirmView,
    UserViewSet, RoleViewSet, PermissionViewSet, UserAddressViewSet
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'addresses', UserAddressViewSet, basename='address')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', UserRegistrationView.as_view(), name='api_register'),
    path('auth/login/', UserLoginView.as_view(), name='api_login'),
    path('auth/logout/', UserLogoutView.as_view(), name='api_logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    
    # Profile management
    path('auth/profile/', UserProfileView.as_view(), name='api_profile'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='api_change_password'),
    
    # Password reset
    path('auth/password-reset/', PasswordResetView.as_view(), name='api_password_reset'),
    path('auth/password-reset-confirm/<str:uid>/<str:token>/', 
         PasswordResetConfirmView.as_view(), name='api_password_reset_confirm'),
    
    # Include router URLs
    path('', include(router.urls)),
]