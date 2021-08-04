from django.contrib import admin
from . models import Order, OrderProduct, Payment, OrderDiscount

# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product',
                       'quantity', 'product_price', 'ordered')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone_number', 'email',
                    'order_total', 'status', 'is_ordered', 'created_at')
    # list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name',
                     'last_name', 'phone_number', 'email']
    list_per_page = 15
    inlines = [OrderProductInline]


class OrderDiscountAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        count = OrderDiscount.objects.all().count()
        if count == 0:
            return True
        return False


# admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderProduct)
admin.site.register(OrderDiscount, OrderDiscountAdmin)
