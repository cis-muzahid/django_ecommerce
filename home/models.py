from django.db import models
from users.models import CustomUser
from products.models import Category
# Create your models here.

class Banner(models.Model):
    title=models.CharField(max_length=255, unique=True)
    subtitle=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    image=models.ImageField(upload_to='banner/images/')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=255) # header banner, middle banner and lower banner
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"

class Facility(models.Model):
    image=models.ImageField(upload_to='facility/images/')
    title=models.CharField(max_length=255)
    active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"
