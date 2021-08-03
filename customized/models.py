from colorfield.fields import ColorField
from django.db import models
from accounts.models import User

# Create your models here.


class CustomizedOrder(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    customized_order_number = models.CharField(max_length=20, blank=True)
    order_type = models.CharField(max_length=150, blank=True)
    front_text = models.CharField(max_length=255, blank=True)
    back_text = models.CharField(max_length=255, blank=True)
    color = ColorField(default='#FF0000')
    logo = models.ImageField(upload_to="customized_orders/", blank=True)
    description = models.TextField()
    quantity = models.IntegerField()
    design_image = models.ImageField(
        upload_to="customized_orders/", blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customized_order_number
