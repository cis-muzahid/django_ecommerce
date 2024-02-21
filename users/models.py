from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# class CustomUserManager(BaseUserManager):

class CustomUser(AbstractUser):
	CUSTOMER = 'customer'
	SUPPLIER = 'supplier'
	ADMIN = 'admin'

	ROLE_CHOICES = [
			(CUSTOMER, 'Customer'),
			(SUPPLIER, 'Supplier'),
			(ADMIN, 'Admin'),
	]

	username = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)

	# objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
			return self.email
	

