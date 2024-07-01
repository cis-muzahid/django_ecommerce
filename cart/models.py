from django.db import models
from users.models import CustomUser
from products.models import Product

# Create your models here.
class Cart(models.Model):
    """ Model class for Cart """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email + " : Cart Product"

class Wishlist(models.Model):
    """ Model class for Wishlist """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email + " : Wishlist"