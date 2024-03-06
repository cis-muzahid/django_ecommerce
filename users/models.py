from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# class CustomUserManager(BaseUserManager):


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


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

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def __str__(self):
			return self.email
	