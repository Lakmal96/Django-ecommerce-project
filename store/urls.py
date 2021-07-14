from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('category/<slug:category_slug>/',
         views.store, name="view_by_category"),
    path('category/<slug:category_slug>/<slug:product_slug>/',
         views.product_detail, name="product_detail"),
    path('search/', views.search, name="search"),
    path('product_review/<int:product_id>/',
         views.product_review, name="product_review")
]
