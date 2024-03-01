from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# class CustomUserManager(BaseUserManager):



class Permission(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Role(models.Model):
	
	name = models.CharField(max_length=20, blank=True, null=True)
	permissions = models.ManyToManyField(Permission)

	def __str__(self):
			return self.name
class CustomUser(AbstractUser):
	
	username = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	# user_role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=customer)
	user_role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)

	# objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
			return self.email
	