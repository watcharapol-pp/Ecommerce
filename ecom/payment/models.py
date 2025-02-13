from django.db import models
from django.contrib.auth.models import User
from store.models import Product


# Create your models here.
class ShippingAddress(models.Model):
    # id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=300)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    city = models.CharField(max_length=100)

    #optionnal
    state = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True)

    

    #FK
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # def __str__(self):

    #     return f"{self.user.username} - {self.address1}, {self.city}, {self.country}"
    # status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    
    class Meta:
        verbose_name_plural = 'Shipping Address'

class Order(models.Model):
    email = models.CharField(max_length=300)
    full_name = models.CharField(max_length=255)
    shipping_address = models.TextField(max_length=1000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    # FK
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return 'Order - #' + str(self.id)
    
class OrderItem(models.Model):
    # FK
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveBigIntegerField(default=1)

    # FK
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return 'Order Item - #' + str(self.id)
    
# class Payment(models.Model):
    # # FK
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    # timestamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.user.username} - {self.amount} - {self.status}"
    
