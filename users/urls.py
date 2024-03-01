from django.urls import path
from .views import LoginView, LogoutView, SignupView, UserIndexView, AddUserView, RoleIndexView, AddRoleView, PermissionIndexView, AddPermissionView, UpdateRoleView, DeleteRoleView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('user/index/', UserIndexView.as_view(), name='user_index'),
    path('user/add/', AddUserView.as_view(), name='add_user'),
    path('role/index', RoleIndexView.as_view(), name='role_index'),
    path('role/add', AddRoleView.as_view(), name='add_role'),
    path('permission/add', AddPermissionView.as_view(), name='add_permission'),
    path('permission/index', PermissionIndexView.as_view(), name='permission_index'),
    path('role/update/<int:role_id>/', UpdateRoleView.as_view(), name='update_role'),
    path('role/delete/<int:role_id>/', DeleteRoleView.as_view(), name='delete_role'),

    # Add more paths as needed for your application
]