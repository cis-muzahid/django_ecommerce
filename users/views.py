from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from .models import CustomUser, Role, Permission
from users.forms import CutomUserForm, UserRoleForm, UserPermissionForm
from django.urls import reverse


# Custom User model
User = get_user_model()

class LoginView(View):
    def get(self, request):
        return render(request, 'authenticate/login.html')

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome, you are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login_user')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class SignupView(View):
    def get(self, request):
        return render(request, "authenticate/signup.html")

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['cnf_password']
        user = User.objects.create_user(email=email, username=username, first_name=first_name, last_name=last_name, password=password)
        user.save()
        print (user.username)
        messages.success(request, 'Your account has been successfully created.')
        return redirect('login_user')

class UserIndexView(generic.TemplateView):
    template_name = 'admin/user_management/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        return context
class AddUserView(View):        
    template_name = 'admin/user_management/create.html'  # Adjust the template name

    def get(self, request):
        form = CutomUserForm()
        roles = Role.objects.all()  # Fetch all roles
        form.fields['user_role'].queryset = roles
        return render(request, self.template_name, {'form': form, 'roles': roles})

    def post(self, request):
        form = CutomUserForm(request.POST)
        print(form.is_valid())
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
class RoleIndexView(View):
    template_name = 'admin/role_management/index.html'

    def get(self, request, *args, **kwargs):
        roles_with_permissions = Role.objects.prefetch_related('permissions').all()
        return render(request, self.template_name, {'roles_with_permissions': roles_with_permissions})
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

    # template_name = 'admin/role_management/update.html'

    def get(self, request, role_id):
        role = get_object_or_404(Role, id=role_id)
        form = UserRoleForm(instance=role)

        # Redirect to the create role view with pre-filled data
        create_role_url = reverse('add_role') + f'?name={role.name}&permissions={",".join(str(perm.id) for perm in role.permissions.all())}'
        return redirect(create_role_url)

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

        return render(request, self.template_name, {'form': form, 'role': role})

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

    def get(self, request):
        permissions = Permission.objects.all()
        return render(request, self.template_name, {'permissions': permissions})

class AddPermissionView(View):
    template_name = 'admin/permission/create.html'

    def get(self, request):
        form = UserPermissionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # breakpoint()
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
