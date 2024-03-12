from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View, generic
from .models import CustomUser, Role, Permission
from users.forms import CutomUserForm, UserRoleForm, UserPermissionForm,LoginForm
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

# Custom User model
User = get_user_model()

class LoginView(View):
    
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
                messages.success(request, 'Welcome, you are now logged in.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials.')
                return redirect('login_user')

class CustomAdminLoginView(View):
    template_name = 'admin/admin_login.html'  # Replace with your admin login template

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
            if user.is_superuser:
                login(request, user)
                messages.success(request, 'Welcome, you are now logged in as admin.')
                return redirect('user_index')  # Redirect superusers to user index
            elif user.user_role.name == 'Supplier':
                login(request, user)
                messages.success(request, 'Welcome, you are now logged in as Supplier.')
                return redirect('/products')
            else:
                messages.error(request, 'Invalid login credentials for admin.')
                return render(request, self.template_name)
        print(form.errors)
        return render(request, self.template_name)

class CustomAdminLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('admin_login')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class SignupView(View):
    def get(self, request):
        try:
            role = Role.objects.get(name='user')
            return render(request, "authenticate/signup.html", {'user_role':role})
        except ObjectDoesNotExist:
            return HttpResponse("User role does not exist. Please check your database setup or create the 'user' role.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}. Please contact the administrator.")

    def post(self, request):
        form = CutomUserForm(request.POST)
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

            messages.success(request, 'Your account has been successfully created.')
            return redirect('login_user')
        else:
            messages.error(request, form.errors)
            return render(request, "authenticate/signup.html")
class UserIndexView(generic.TemplateView):
    template_name = 'admin/user_management/index.html'
    paginate_by = 10
    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        paginator = Paginator(users, self.paginate_by)
        page_number = request.GET.get('page')
        users_page = paginator.get_page(page_number)

        return render(request, self.template_name, {'users': users_page})
    
class AddUserView(View):        
    template_name = 'admin/user_management/create.html'  # Adjust the template name

    def get(self, request):
        form = CutomUserForm()
        roles = Role.objects.all()  # Fetch all roles
        form.fields['user_role'].queryset = roles
        return render(request, self.template_name, {'form': form, 'roles': roles})

    def post(self, request):
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
        user = CustomUser.objects.get(id=user_id)
        form = CutomUserForm(instance=user)
        roles = Role.objects.all()  # Fetch all roles
        form.fields['user_role'].queryset = roles
        return render(request, self.template_name, {'form': form, 'roles': roles, 'user': user})

    def post(self, request, user_id):
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
        user = get_object_or_404(User, id=user_id)
        try:
            user.delete()
            messages.success(request, 'Role has been successfully deleted.')
        except Exception as e:
            messages.error(request, f'Error deleting role: {str(e)}')

        return redirect('user_index')
class RoleIndexView(View):
    template_name = 'admin/role_management/index.html'
    paginate_by = 5 
    def get(self, request, *args, **kwargs):
        roles_with_permissions = Role.objects.prefetch_related('permissions').all()
        paginator = Paginator(roles_with_permissions, self.paginate_by)
        page_number = request.GET.get('page')
        roles_page = paginator.get_page(page_number)

        return render(request, self.template_name, {'roles_with_permissions': roles_page})
class AddRoleView(View):
    template_name = 'admin/role_management/create.html'

    def get(self, request):
        all_permissions = Permission.objects.all()
        return render(request, self.template_name, {'all_permissions': all_permissions})

    def post(self, request):
        try:
            role_name = request.POST.get('role_name')
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
        role = get_object_or_404(Role, id=role_id)
        form = UserRoleForm(instance=role)
        return render(request, self.template_name, {'form': form, 'role': role, 'all_permissions': Permission.objects.all()})

    def post(self, request, role_id):
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

    def post(self, request, role_id):
        role = get_object_or_404(Role, id=role_id)
        try:
            role.delete()
            messages.success(request, 'Role has been successfully deleted.')
        except Exception as e:
            messages.error(request, f'Error deleting role: {str(e)}')

        return redirect('role_index')
    
class PermissionIndexView(View):
    template_name = 'admin/permission/index.html'
    paginate_by = 10  # Set the number of permissions per page

    def get(self, request, *args, **kwargs):
        permissions_list = Permission.objects.all()
        paginator = Paginator(permissions_list, self.paginate_by)
        page_number = request.GET.get('page')
        permissions_page = paginator.get_page(page_number)

        return render(request, self.template_name, {'permissions': permissions_page})

class AddPermissionView(View):
    template_name = 'admin/permission/create.html'

    def get(self, request):
        form = UserPermissionForm()
        return render(request, self.template_name, {'form': form})

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
    template_name = 'admin/permission/update.html'  # Adjust the template name

    def get(self, request, perm_id):
        permission = get_object_or_404(Permission, id=perm_id)
        form = UserPermissionForm(instance=permission)
        return render(request, self.template_name, {'form': form, 'permission': permission})

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
    template_name = 'admin/permission/delete.html'  # Adjust the template name

    def post(self, request, perm_id):
        permission = get_object_or_404(Permission, id=perm_id)
        try:
            permission.delete()
            messages.success(request, 'Permission has been successfully deleted.')
        except Exception as e:
            messages.error(request, f'Error deleting permission: {str(e)}')

        return redirect('permission_index')
    
