from django.db import models
from users.models import CustomUser
from cart.models import Cart

# Create your models here.
class Order(models.Model):
    ORDER_STATUS = (
        ('initial', 'Initial'),
        ('in_process', 'In Process'),
        ('deliverd', 'Deliverd'),
        ('replace', 'Replace'),
        ('return', 'Return'),
        ('cancled', 'Cancle'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices=ORDER_STATUS, default='initial')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255, default=None)
    payment_status= models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.email}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f"OrderItem #{self.pk} - {self.cart.product.name}"