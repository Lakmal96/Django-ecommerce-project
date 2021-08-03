from django.contrib import admin
from . models import CustomizedOrder

# Register your models here.


class CustomizedOrderAdmin(admin.ModelAdmin):
    list_display = ('customized_order_number', 'order_type',
                    'quantity', 'status', 'created_at')


admin.site.register(CustomizedOrder, CustomizedOrderAdmin)
