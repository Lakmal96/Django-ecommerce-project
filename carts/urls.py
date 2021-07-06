from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('add_to_cart/<int:product_id>/',
         views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:product_id>/<int:cart_item_id>/',
         views.remove_from_cart, name="remove_from_cart"),
    path('remove_all_cart/<int:product_id>/<int:cart_item_id>/',
         views.remove_all_cart, name="remove_all_cart"),
    path('checkout/', views.checkout, name="checkout"),

]
