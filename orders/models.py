from django.db import models
from users.models import CustomUser
from cart.models import Cart

# Create your models here.
class Order(models.Model):
    ORDER_STATUS = (
        ('initial', 'initial'),
        ('in_process', 'In Process'),
        ('deliverd', 'Deliverd'),
        ('replace', 'Replace'),
        ('return', 'Return'),
        ('cancled', 'Cancle'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=ORDER_STATUS)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=20, default=None)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.email}"