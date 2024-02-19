from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

# Create your views here.
class Login:
	def login_user(request):
		if request.method =="POST":
				username = request.POST["username"]
				password = request.POST["password"]
				user = authenticate(request, username=username, password=password)
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
		