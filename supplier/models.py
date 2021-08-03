from django.db import models
from accounts.models import User
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField

# Create your models here.


class SupplierOrder(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Completed', 'Completed'),
    )

    supplier = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_type = models.CharField(max_length=150, blank=True)
    front_text = models.CharField(max_length=255, blank=True)
    back_text = models.CharField(max_length=255, blank=True)
    color = ColorField(default='#FF0000')
    quantity = models.IntegerField()
    design_image = models.ImageField(
        upload_to="supplier_customized_orders/", blank=True)
    description = RichTextField()
    status = models.CharField(max_length=10, choices=STATUS, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_type
