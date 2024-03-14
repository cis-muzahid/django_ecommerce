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
        ('cancelled', 'Cancle'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices=ORDER_STATUS, default='initial')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255, default=None)
    payment_status= models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField( auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"OrderItem #{self.pk} - {self.cart.product.name}"
    
class ReturnAndReplaceOrder(models.Model):
    order = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='order_return_replace')
    requested = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    reason = models.TextField(blank=True)
    action = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField( auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True,blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} : {self.order.id} - {self.action}"
