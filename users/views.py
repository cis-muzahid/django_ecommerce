from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View, generic
from .models import CustomUser, Role, Permission
from products.models import Product
from orders.models import Order
from users.forms import CutomUserForm, UserRoleForm, UserPermissionForm, LoginForm, AddressForm
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from orders.utilities import fetch_user_address
from users.models import UserAddress

# Custom User model
User = get_user_model()

class LoginView(View):
    """ user login view """
    def get(self, request):
        return render(request, 'authenticate/login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            print('user', user)
            if user is not None:
                login(request, user)
                if user.is_superuser or (user.user_role and user.user_role.name == 'admin'):
                    messages.success(request, 'Welcome, you are now logged in as Admin.')
                    return redirect('/admin')
                elif user.user_role and user.user_role.name == 'supplier':
                    messages.success(request, 'Welcome, you are now logged in as Supplier.')
                    return redirect('/products')
                else:
                    messages.success(request, 'Welcome, you are now logged.')
                    return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials.')
                return redirect('login_user')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login_user')

class CustomAdminLoginView(View):
    """ admin login view """
    template_name = 'admin/admin_login.html'

    def get(self, request):
        return render(request,self.template_name )

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            # user = form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            print('user', user)
            if user.is_superuser or user.user_role.name == 'admin':
                login(request, user)
                messages.success(request, 'Welcome, you are now logged in as admin.')
                return redirect('user_index')  # Redirect superusers to user index
            elif request.user.user_role and user.user_role.name == 'supplier':
                login(request, user)
                messages.success(request, 'Welcome, you are now logged in as Supplier.')
                return redirect('/products')
            else:
                messages.error(request, 'Invalid login credentials for admin.')
                return render(request, self.template_name)
        print(form.errors)
        return render(request, self.template_name)

class CustomAdminLogoutView(View):
    """ admin logout view """
    def get(self, request):
        logout(request)
        return redirect('admin_login')

class LogoutView(View):
    """ user logout view """
    def get(self, request):
        logout(request)
        return redirect('home')

class SignupView(View):
    def get(self, request):
        """ user signup form view """
        try:
            roles = Role.objects.exclude(name='admin')
            return render(request, "authenticate/signup.html", {'user_roles':roles})
        except ObjectDoesNotExist:
            return HttpResponse("User role does not exist. Please check your database setup or create the 'user' role.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}. Please contact the administrator.")

    def post(self, request):
        """ user ragistration view """
        form = CutomUserForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                mobile_no=form.cleaned_data['mobile_no']
            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.user_role = form.cleaned_data['user_role']
            user.save()

            messages.success(request, 'Your account has been successfully created. Please login to continue!!')
            return redirect('login_user')
        else:
            roles = Role.objects.exclude(name='admin')
            return render(request, "authenticate/signup.html", { 'errors': form.errors, 'user_roles': roles })

class UserIndexView(generic.TemplateView):
    """ users list for admin """
    template_name = 'admin/user_management/index.html'
    paginate_by = 10
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            users = CustomUser.objects.all()
            paginator = Paginator(users, self.paginate_by)
            page_number = request.GET.get('page')
            users_page = paginator.get_page(page_number)

            return render(request, self.template_name, {'users': users_page})
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('admin_login')

class AddUserView(View):
    """ view that allow admin to add user """
    template_name = 'admin/user_management/create.html'  # Adjust the template name

    def get(self, request):
        """ create user form view """
        if request.user.is_authenticated:
            form = CutomUserForm()
            roles = Role.objects.all()  # Fetch all roles
            form.fields['user_role'].queryset = roles
            return render(request, self.template_name, {'form': form, 'roles': roles})
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('admin_login')

    def post(self, request):
        """ create user view from admin dashboard """
        form = CutomUserForm(request.POST)
        try:
            if form.is_valid():
                role = form.cleaned_data['user_role']
                user = CustomUser.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.user_role = role
                user.save()
                messages.success(request, 'User account has been successfully created.')
                return redirect('user_index')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
        
        roles = Role.objects.all()  # Fetch all roles
        return render(request, self.template_name, {'form': form, 'roles': roles})

class UserUpdateView(View):
    template_name = 'admin/user_management/update.html'  # Use the same template as AddUserView

    def get(self, request, user_id):
        """ form for update user by admin """
        if request.user.is_authenticated:
            user = CustomUser.objects.get(id=user_id)
            form = CutomUserForm(instance=user)
            roles = Role.objects.all()  # Fetch all roles
            form.fields['user_role'].queryset = roles
            return render(request, self.template_name, {'form': form, 'roles': roles, 'user': user})
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('admin_login')

    def post(self, request, user_id):
        """ update view for user from admin dashboard """
        try:
            user = CustomUser.objects.get(id=user_id)
            form = CutomUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'User account has been successfully updated.')
                return redirect('user_index')
            else:
                roles = Role.objects.all()  # Fetch all roles
                return render(request, self.template_name, {'form': form, 'roles': roles, 'user': user})
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found.')
        except Exception as e:
            messages.error(request, f'Error updating user account: {str(e)}')

        return redirect('user_index')

class UserDeleteView(View):
    def post(self, request, user_id):
        """ user delete view for user """
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=user_id)
            try:
                user.delete()
                messages.success(request, 'Role has been successfully deleted.')
            except Exception as e:
                messages.error(request, f'Error deleting role: {str(e)}')

            return redirect('user_index')
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('admin_login')

class RoleIndexView(View):
    """ roles list view for user """
    template_name = 'admin/role_management/index.html'
    paginate_by = 5 
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            roles_with_permissions = Role.objects.prefetch_related('permissions').all()
            paginator = Paginator(roles_with_permissions, self.paginate_by)
            page_number = request.GET.get('page')
            roles_page = paginator.get_page(page_number)

            return render(request, self.template_name, {'roles_with_permissions': roles_page})
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('admin_login')

class AddRoleView(View):
    """ view that allow admin to add roles """
    template_name = 'admin/role_management/create.html'
    def get(self, request):
        """ role create form """
        if request.user.is_authenticated:
            all_permissions = Permission.objects.all()
            return render(request, self.template_name, {'all_permissions': all_permissions})
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('admin_login')

    def post(self, request):
        """ role create view """
        try:
            role_name = request.POST.get('role_name').lower()
            selected_permissions = request.POST.getlist('permissions')

            new_role = Role.objects.create(name=role_name)
            new_role.permissions.set(selected_permissions)

            messages.success(request, 'Role has been successfully created.')
            return redirect('role_index')
        except Exception as e:
            messages.error(request, f'Error creating role: {str(e)}')

        all_permissions = Permission.objects.all()
        return render(request, self.template_name, {'all_permissions': all_permissions})

class UpdateRoleView(View):
    template_name = 'admin/role_management/update.html'
    def get(self, request, role_id):
        """ update role form view """
        if request.user.is_authenticated:
            role = get_object_or_404(Role, id=role_id)
            form = UserRoleForm(instance=role)
            return render(request, self.template_name, {'form': form, 'role': role, 'all_permissions': Permission.objects.all()})
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('admin_login')

    def post(self, request, role_id):
        """ update role view """
        role = get_object_or_404(Role, id=role_id)
        form = UserRoleForm(request.POST, instance=role)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Role has been successfully updated.')
                return redirect('role_index')
        except Exception as e:
            messages.error(request, f'Error updating role: {str(e)}')
        return render(request, self.template_name, {'form': form, 'role': role, 'all_permissions': Permission.objects.all()})

class DeleteRoleView(View):
    """ delete role view """
    def post(self, request, role_id):
        if request.user.is_authenticated:
            role = get_object_or_404(Role, id=role_id)
            try:
                role.delete()
                messages.success(request, 'Role has been successfully deleted.')
            except Exception as e:
                messages.error(request, f'Error deleting role: {str(e)}')

            return redirect('role_index')
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('admin_login')

class PermissionIndexView(View):
    """ permission list view for admin """
    template_name = 'admin/permission/index.html'
    paginate_by = 10  # Set the number of permissions per page

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            permissions_list = Permission.objects.all()
            paginator = Paginator(permissions_list, self.paginate_by)
            page_number = request.GET.get('page')
            permissions_page = paginator.get_page(page_number)

            return render(request, self.template_name, {'permissions': permissions_page})
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('admin_login')

class AddPermissionView(View):
    """ permission create view by admin """
    template_name = 'admin/permission/create.html'

    def get(self, request):
        if request.user.is_authenticated:
            form = UserPermissionForm()
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('admin_login')

    def post(self, request):
        form = UserPermissionForm(request.POST)
        try:
            if form.is_valid():
                permission = form.cleaned_data['name']
                new_permission = Permission.objects.create(name=permission)
                messages.success(request, 'Permission has been successfully created.')
                return redirect('permission_index')
                # return render(request, self.template_name, {'form': form})
        except Exception as e:
            messages.error(request, f'Error creating permission: {str(e)}')
        
        return render(request, self.template_name, {'form': form})

class UpdatePermissionView(View):
    """ permission update view for admin """
    template_name = 'admin/permission/update.html'  # Adjust the template name

    def get(self, request, perm_id):
        if request.user.is_authenticated:
            permission = get_object_or_404(Permission, id=perm_id)
            form = UserPermissionForm(instance=permission)
            return render(request, self.template_name, {'form': form, 'permission': permission})
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('admin_login')

    def post(self, request, perm_id):
        permission = get_object_or_404(Permission, id=perm_id)
        form = UserPermissionForm(request.POST, instance=permission)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Permission has been successfully updated.')
                return redirect('permission_index')
        except Exception as e:
            messages.error(request, f'Error updating permission: {str(e)}')

        return render(request, self.template_name, {'form': form, 'permission': permission})

class DeletePermissionView(View):
    """ permission delete view """
    template_name = 'admin/permission/delete.html'  # Adjust the template name

    def post(self, request, perm_id):
        if request.user.is_authenticated:
            permission = get_object_or_404(Permission, id=perm_id)
            try:
                permission.delete()
                messages.success(request, 'Permission has been successfully deleted.')
            except Exception as e:
                messages.error(request, f'Error deleting permission: {str(e)}')

            return redirect('permission_index')
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('admin_login')

class AdminDashboardView(View):
    """ admin dashboard view """
    template_name = 'admin/dashboard.html'
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser or (request.user.user_role and request.user.user_role.name == 'admin'):
                users = CustomUser.objects.all()
                products = Product.objects.all()
                orders = Order.objects.all()
                return render(request, self.template_name, {'users': users, 'products': products, 'orders': orders})
            else:
                messages.error(request, 'Sorry, you are not authorized to access this page.')
                return redirect('home')
        else:
            return redirect('admin_login')

class UserProfileView(View):
    template_name = 'authenticate/profile.html'
    def get(self, request):
        """ user profile view """
        if request.user.is_authenticated:
            addresses = fetch_user_address(request.user)
            return render(request, self.template_name, {'addresses': addresses })
        else:
            messages.error(request, 'Sorry, you are not authorized to access this page.')
            return redirect('login_user')
    
    def post(self, request):
        """ update user profile view """
        form = CutomUserForm(request.POST, request.FILES, instance=request.user)
        addresses = fetch_user_address(request.user)
        try:
            if form.is_valid():
                form.save()
            else:
                messages.error(request, f"Facing issue with this request : { form.errors }")
            return redirect('user_profile')
        except Exception as e:
            messages.error(request, f"Facing issue with this request : { e }")
            return render(request, 'authenticate/profile.html', { 'addresses': addresses })

class UserUpdateAddressView(View):
    def post(self, request):
        """ update user address view """
        addresses = fetch_user_address(request.user)
        try:
            address = UserAddress.objects.get(id=request.POST.get('address', 'None'))
        except UserAddress.DoesNotExist:
            return render(request, 'authenticate/profile.html', { 'addresses': addresses })
        
        form = AddressForm(request.POST, instance=address)
        try:
            if form.is_valid():
                if request.POST.get('is_default',None) == 'True':
                    UserAddress.objects.filter(user=request.user).update(is_default=False)
                form.save()

            return redirect('user_profile')
        except:
            return render(request, 'authenticate/profile.html', {'form': form, 'addresses': addresses })

class DeleteAddressView(View):
    """ user address delete view """
    def post(self, request):
        try:
            address = UserAddress.objects.get(id=request.POST.get('address', 'None'))
            address.delete()
            return redirect('user_profile')
        except:
            addresses = fetch_user_address(request.user)
            messages.error(request, f'Error Address deleting')
            return render(request, 'authenticate/profile.html', { 'addresses': addresses })
