from django.db import models
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    is_delete = models.BooleanField(null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="Weight in kilograms")
    length = models.DecimalField(max_digits=10, decimal_places=2, help_text="Length in centimeters")
    width = models.DecimalField(max_digits=10, decimal_places=2, help_text="Width in centimeters")
    height = models.DecimalField(max_digits=10, decimal_places=2, help_text="Height in centimeters")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_delete = models.BooleanField(null=True)
    created_at = models.DateTimeField( auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to='static/images', blank=True, null=True )
    out_of_stoke = models.BooleanField(default=False)
    is_display =  models.BooleanField(default=True)
    is_delete = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.product.name} - {self.title}: {self.value}"


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_delete = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.product.name} - {self.title}: {self.description}"
