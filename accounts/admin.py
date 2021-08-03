from django.contrib import admin
from . models import User, Customer, Supplier
from django.contrib.auth.models import Group

# Register your models here.

admin.site.register(User)

admin.site.register(Customer)

admin.site.register(Supplier)

admin.site.unregister(Group)
