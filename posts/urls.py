from django.urls import path
from . import views

urlpatterns = [
    path('', views.fashion_tips, name="fashion_tips"),
]
