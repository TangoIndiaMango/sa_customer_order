from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from .validators import validate_phone_number

class Customer(models.Model):
    user = models.ForeignKey(User, related_name='customers', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"