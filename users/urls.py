from django.urls import path
from .views import LoginView, LogoutView, SignupView, UserIndexView, AddUserView, RoleIndexView, AddRoleView, PermissionIndexView, AddPermissionView, UpdateRoleView, DeleteRoleView, UserDeleteView, UserUpdateView, UpdatePermissionView, DeletePermissionView, CustomAdminLoginView, CustomAdminLogoutView

urlpatterns = [
    path('admin_login/', CustomAdminLoginView.as_view(), name='admin_login'),
    path('admin_logout/', CustomAdminLogoutView.as_view(), name='admin_logout'),
    # path('admin/', admin_redirect, name='admin_redirect'),
    
    path('login_user/', LoginView.as_view(), name='login_user'),
    path('logout_user/', LogoutView.as_view(), name='logout_user'),
    path('signup_user/', SignupView.as_view(), name='signup_user'),

    path('user/index/', UserIndexView.as_view(), name='user_index'),
    path('user/add/', AddUserView.as_view(), name='add_user'),
    path('user/update/<int:user_id>/', UserUpdateView.as_view(), name='update_user'),
    path('user/delete/<int:user_id>/', UserDeleteView.as_view(), name='delete_user'),

    path('role/index', RoleIndexView.as_view(), name='role_index'),
    path('role/add', AddRoleView.as_view(), name='add_role'),
    path('role/update/<int:role_id>/', UpdateRoleView.as_view(), name='update_role'),
    path('role/delete/<int:role_id>/', DeleteRoleView.as_view(), name='delete_role'),

    path('permission/add', AddPermissionView.as_view(), name='add_permission'),
    path('permission/index', PermissionIndexView.as_view(), name='permission_index'),
    path('permission/delete/<int:perm_id>/', DeletePermissionView.as_view(), name='delete_permission'),
    path('permission/update/<int:perm_id>/', UpdatePermissionView.as_view(), name='update_permission'),

    # Add more paths as needed for your application
]