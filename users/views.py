from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import CustomUser
# Create your views here.
class Login:
	def login_user(request):
		if request.method =="POST":
			email = request.POST["email"]
			password = request.POST["password"]
			user = authenticate(request, email=email, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, 'Welcome login user.')
				return redirect('home')
				# Redirect to a success page.
				...
			else:
				messages.info(request, 'user does not exist.')
				return redirect('login')
				# Return an 'invalid login' error message.
				...
		else:
			return render(request, 'authenticate/login.html', {})

	def logout_user(request):
		logout(request)
		return redirect('home')

	def signup_user(request):
		if request.method =="POST":
			User = get_user_model()
			# breakpoint()
			user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
			user.first_name = request.POST['firstname']
			user.last_name = request.POST['lastname']
			user.save()
			messages.success(request, 'Your accout has been successfully created.')
			return redirect('login')
		else:
			return render(request, "authenticate/signup.html")

class AdminView(generic.TemplateView):
	template_name: str = 'admin/home.html'

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
