from django.shortcuts import render, redirect
from orders.models import Order
from accounts.models import User, Customer, Supplier
from customized.models import CustomizedOrder
from store.models import Product
from category.models import Category
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages

# Create your views here.


def sales_data(request):

    orders = Order.objects.filter(is_ordered=True)
    completed_orders = Order.objects.filter(
        is_ordered=True, status="Completed")
    new_orders = Order.objects.filter(is_ordered=True, status="New")
    customized_orders_new = CustomizedOrder.objects.filter(
        status="Pending")
    customized_orders = CustomizedOrder.objects.all()
    customized_orders_accepted = CustomizedOrder.objects.filter(
        status="Accepted")
    users = User.objects.exclude(is_superuser=True)
    customers = Customer.objects.all()
    suppliers = Supplier.objects.all()

    order_count = orders.count()
    completed_orders_count = completed_orders.count()
    new_orders = new_orders.count()
    customized_count = customized_orders.count()
    new_customized_count = customized_orders_new.count()
    accepted_customized_count = customized_orders_accepted.count()
    user_count = users.count()
    customer_count = customers.count()
    supplier_count = suppliers.count()

    context = {
        'orders': orders,
        'order_count': order_count,
        'new_orders': new_orders,
        'completed_orders_count': completed_orders_count,
        'new_customized_count': new_customized_count,
        'customized_count': customized_count,
        'accepted_customized_count': accepted_customized_count,
        'user_count': user_count,
        'customer_count': customer_count,
        'supplier_count': supplier_count,
    }

    return render(request, 'reports/sales_data.html', context)


def by_date(request):

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        orders_by_date = Order.objects.filter(
            created_at__range=[start_date, end_date], is_ordered=True)

        if start_date > end_date:
            messages.error(request, "Please enter Valid Date Range")
            return redirect("by_date")

        # if start_date == "":
        #     messages.error(request, "Please Select a Start Date")
        #     return redirect("by_date")

        # if end_date == "":
        #     messages.error(request, "Please Select a End Date")
        #     return redirect("by_date")

        # if start_date == "" and end_date == "":
        #     messages.error(request, "Please Select a Date Range")
        #     return redirect("by_date")

        sub_total = 0
        for i in orders_by_date:
            sub_total += i.order_total

        context = {
            'orders_by_date': orders_by_date,
            'start_date': start_date,
            'end_date': end_date,
            'sub_total': sub_total,

        }

        return render(request, 'reports/by_date.html', context)

    else:
        return render(request, 'reports/by_date.html')


def by_date_customized(request):

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        orders_by_date = CustomizedOrder.objects.filter(
            created_at__range=[start_date, end_date])

        context = {
            'orders_by_date': orders_by_date,
            'start_date': start_date,
            'end_date': end_date,

        }

        return render(request, 'reports/by_date_customized.html', context)

    return render(request, 'reports/by_date_customized.html')


def stock(request):
    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'reports/stock_data.html', context)
