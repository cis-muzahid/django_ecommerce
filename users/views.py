from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View, generic
from .models import CustomUser, Role, Permission
from users.forms import CutomUserForm, UserRoleForm, UserPermissionForm



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
            return redirect('login')

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
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        role = request.POST['role']

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, role=role)
        messages.success(request, 'Your account has been successfully created.')
        return redirect('login')

class UserIndexView(generic.TemplateView):
    template_name = 'admin/user_management/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        return context
class AddUserView(View):
    # def get(self, request):
    #     return render(request, 'admin/user_management/create.html')

    # def post(self, request):
    #     form = CutomUserForm(request.POST)
    #     if form.is_valid():
    #         role = request.POST.get('role', None)
    #         user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    #         user.first_name = request.POST['firstname']
    #         user.last_name = request.POST['lastname']
    #         user.role = role
    #         user.save()
    #         messages.success(request, 'User account has been successfully created.')
    #         return redirect('user_index')
        
    template_name = 'admin/user_management/create.html'  # Adjust the template name

    def get(self, request):
        form = CutomUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        
        form = CutomUserForm(request.POST)
        try:
            if form.is_valid():
                role = form.cleaned_data['role'].strip().lower()
                if role not in dict(CustomUser.ROLE_CHOICES).keys():
                    raise ValueError('Invalid role choice')
                user = CustomUser.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.role = role
                user.save()
                messages.success(request, 'User account has been successfully created.')
                return render(request, self.template_name, {'form': form})
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
        
        return render(request, self.template_name, {'form': form})

class RoleIndexView(View):
    template_name = 'admin/role_management/index.html'

    def get(self, request):
        roles = Role.objects.all()
        return render(request, self.template_name, {'roles': roles})

class AddRoleView(View):
    template_name = 'admin/role_management/create.html'

    def get(self, request):
        form = RoleForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RoleForm(request.POST)
        try:
            if form.is_valid():
                role = form.cleaned_data['name']
                new_role = Role.objects.create(name=role)
                messages.success(request, 'Role has been successfully created.')
                return redirect('role_index')
        except Exception as e:
            messages.error(request, f'Error creating role: {str(e)}')
        
        return render(request, self.template_name, {'form': form})

# class PermissionIndexView(View):
#     template_name = 'admin/role_management/permission_index.html'

#     def get(self, request):
#         permissions = Permission.objects.all()
#         return render(request, self.template_name, {'permissions': permissions})

# class AddPermissionView(View):
#     template_name = 'admin/user_management/create_permission.html'

#     def get(self, request):
#         form = PermissionForm()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = PermissionForm(request.POST)
#         try:
#             if form.is_valid():
#                 permission = form.cleaned_data['name']
#                 new_permission = Permission.objects.create(name=permission)
#                 messages.success(request, 'Permission has been successfully created.')
#                 return redirect('permission_index')
#         except Exception as e:
#             messages.error(request, f'Error creating permission: {str(e)}')
        
#         return render(request, self.template_name, {'form': form})
			