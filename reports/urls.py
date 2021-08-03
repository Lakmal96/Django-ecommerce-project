from django.urls import path
from . import views

urlpatterns = [
    path('', views.sales_data, name="sales_data"),
    path('by_date/', views.by_date, name="by_date"),
    path('by_date_customized/', views.by_date_customized,
         name="by_date_customized"),
    path('stock/', views.stock, name="stock"),
]
