from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from . forms import CustomerSignUpForm, SupplierSignUpForm
from . models import User, Customer, Supplier

from carts.views import _cart_id
from carts.models import Cart, CartItem
from orders.models import Order, OrderProduct
from customized.models import CustomizedOrder
from customized.forms import CustomizedOrderForm

import requests

# Create your views here.


def select_role(request):
    return render(request, 'accounts/select_role.html', {})


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'accounts/customer_register.html'

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('/accounts/login')


class SupplierSignUpView(CreateView):
    model = User
    form_class = SupplierSignUpForm
    template_name = 'accounts/supplier_register.html'

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('/accounts/login')


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    if CartItem.objects.filter(cart=cart).exists():
                        cart_item = CartItem.objects.filter(cart=cart)

                        # getting product variation by cart id
                        product_variation = []
                        for item in cart_item:
                            variation = item.variations.all()
                            product_variation.append(list(variation))

                        # get the cart items from the user
                        cart_item = CartItem.objects.filter(user=user)
                        existing_variation_list = []
                        c_item_id = []
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            existing_variation_list.append(
                                list(existing_variation))
                            c_item_id.append(item.id)

                        for pv in product_variation:
                            if pv in existing_variation_list:
                                index = existing_variation_list.index(pv)
                                item_id = c_item_id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()

                except:
                    pass

                login(request, user)
                # HTTP_REFERE will grab the previous url came
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    param = dict(x.split("=") for x in query.split('&'))
                    if 'next' in param:
                        nextPage = param['next']
                        return redirect(nextPage)
                except:
                    return redirect('/')

            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html', context={'form': AuthenticationForm()})


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboad(request):
    orders = Order.objects.order_by(
        '-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    customized_orders = CustomizedOrder.objects.filter(user_id=request.user.id)
    customized_order_count = customized_orders.count()

    context = {
        'orders_count': orders_count,
        'customized_order_count': customized_order_count
    }

    return render(request, 'accounts/dashboard.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            current_site = get_current_site(request)
            email_subject = "Reset your password"
            message = render_to_string('accounts/reset_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, "Password reset email has been sent to your email address")
            return redirect('login')

        else:
            messages.error(request, "Account does not exists")
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please reset your password")
        return redirect('reset_password')

    else:
        messages.error(request, "This link has been expired")
        return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Successfully reset the password")
            return redirect('login')

        else:
            messages.error(request, "Password not match")
            return redirect('reset_password')
    else:
        return render(request, 'accounts/reset_password_page.html')


def my_orders(request):
    orders = Order.objects.order_by(
        '-created_at').filter(user=request.user, is_ordered=True)

    context = {
        'orders': orders
    }

    return render(request, 'accounts/my_orders.html', context)


def my_customized_orders(request):
    customized_orders = CustomizedOrder.objects.filter(
        user=request.user).order_by('-created_at')

    context = {
        'customized_orders': customized_orders
    }

    return render(request, 'accounts/my_customized_orders.html', context)


@login_required(login_url='login')
def order_details(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    sub_total = 0
    for i in order_detail:
        sub_total += i.product_price * i.quantity
    context = {
        'order_detail': order_detail,
        'order': order,
        'sub_total': sub_total,
    }

    return render(request, 'accounts/order_details.html', context)


def customized_order_details(request, customized_order_id):
    customized_order_detail = CustomizedOrder.objects.filter(
        customized_order_number=customized_order_id)

    context = {
        'customized_order_detail': customized_order_detail,
    }

    return render(request, 'accounts/customized_order_details.html', context)
