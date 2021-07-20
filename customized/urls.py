from django.urls import path
from . import views

urlpatterns = [
    path('', views.customized_orders, name="customized_orders"),
]
