from django.db import models
from products.models import Category
from users.models import CustomUser

# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner/images/', blank=True, null=True )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Facility(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='banner/images/', blank=True, null=True )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)