from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_order, name="supplier_order"),
    path('<int:id>/', views.supplier_order_detail, name="supplier_order_detail"),
]
