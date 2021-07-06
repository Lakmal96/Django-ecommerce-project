from django.urls import path
from . import views
from accounts.views import CustomerSignUpView, SupplierSignUpView

urlpatterns = [
    path('register/', views.select_role, name='select_role'),
    path('register_customer/', CustomerSignUpView.as_view(), name="customer_signup"),
    path('register_supplier/', SupplierSignUpView.as_view(), name="supplier_signup"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('dashboard/', views.dashboad, name="dashboard"),
    path('', views.dashboad, name="dashboard"),
    path('forgot_password', views.forgot_password, name="forgot_password"),
    path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate,
         name="reset_password_validate"),
    path('reset_password', views.reset_password, name="reset_password"),
]
