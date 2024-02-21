from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View, generic
from .models import CustomUser

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

class AddUserView(View):
    def get(self, request):
        return render(request, 'admin/user_management/create.html')

    def post(self, request):
        role = request.POST.get('role', None)
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.role = role
        user.save()
        messages.success(request, 'User account has been successfully created.')
        return redirect('user_index')

			

# @login_required
# def create_user(request):
#     if request.method == "POST":
#         # Check if the logged-in user has the required permissions to create a user
#         if request.user.has_perm('auth.add_customuser'):
#             User = get_user_model()
#             user = User.objects.create_user(...)
#             # Assign role based on the form input
#             user.role = request.POST['role']
#             user.save()
#             messages.success(request, 'User created successfully.')
#             return redirect('user_list')
#         else:
#             messages.error(request, 'You do not have permission to create a user.')
#             return redirect('home')
#     else:
#         return render(request, "authenticate/create_user.html")

# @login_required
# def user_list(request):
#     # Check if the logged-in user has the required permissions to view user list
#     if request.user.has_perm('auth.view_customuser'):
#         users = CustomUser.objects.all()
#         return render(request, "authenticate/user_list.html", {'users': users})
#     else:
#         messages.error(request, 'You do not have permission to view user list.')
#         return redirect('home')

# @login_required
# def edit_user(request, user_id):
#     # Check if the logged-in user has the required permissions to edit a user
#     if request.user.has_perm('auth.change_customuser'):
#         user = CustomUser.objects.get(pk=user_id)
#         if request.method == "POST":
#             # Update user fields and role based on the form input
#             user.email = request.POST['email']
#             user.first_name = request.POST['first_name']
#             user.last_name = request.POST['last_name']
#             user.role = request.POST['role']
#             user.save()
#             messages.success(request, 'User updated successfully.')
#             return redirect('user_list')
#         else:
#             return render(request, "authenticate/edit_user.html", {'user': user})
#     else:
#         messages.error(request, 'You do not have permission to edit this user.')
#         return redirect('home')

# @login_required
# def delete_user(request, user_id):
#     # Check if the logged-in user has the required permissions to delete a user
#     if request.user.has_perm('auth.delete_customuser'):
#         user = CustomUser.objects.get(pk=user_id)
#         user.delete()
#         messages.success(request, 'User deleted successfully.')
#         return redirect('user_list')
#     else:
#         messages.error(request, 'You do not have permission to delete this user.')
#         return redirect('home')
		

		
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# @permission_required('users.delete_customuser')
# def delete_user(request):
# 	"""
# 	delete requested user
# 	"""
