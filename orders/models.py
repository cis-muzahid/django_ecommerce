from django.db import models
from users.models import CustomUser
from cart.models import Cart

# Create your models here.
class Order(models.Model):
    """ Model class for Order """
    ORDER_STATUS = (
        ('initial', 'Initial'),
        ('in_process', 'In Process'),
        ('deliverd', 'Deliverd'),
        ('replace', 'Replace'),
        ('return', 'Return'),
        ('cancelled', 'Cancle'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=255, choices=ORDER_STATUS, default='initial')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255, default=None)
    payment_method = models.CharField(max_length=255, default='none')
    payment_id = models.CharField(max_length=255, default='none')
    payment_status = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.email}"

class OrderItem(models.Model):
    """ Model class for Order Items """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"OrderItem #{self.pk} - {self.cart.product.name}"
    
class ReturnAndReplaceOrder(models.Model):
    """ Model class for Return and Replace Order """
    order = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='order_return_replace')
    requested = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    reason = models.TextField(blank=True)
    action = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField( auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True,blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    # tracking_number = models.CharField(max_length=255, default=None, null=True)


    def __str__(self):
        return f"{self.user.email} : {self.order.id} - {self.action}"


class CartOrderItem(models.Model):
    """ Model class for storing cart items if user choose stripe payment """

    active = models.BooleanField(default=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.pk} - {self.order.user.email}"
