from django.shortcuts import render, redirect, HttpResponse
from . forms import CustomizedOrderForm
from . models import CustomizedOrder
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='login')
def customized_orders(request):
    current_user = request.user

    if request.method == 'POST':
        form = CustomizedOrderForm(request.POST, request.FILES)
        if form.is_valid():
            data = CustomizedOrder()
            data.user = current_user
            data.order_type = form.cleaned_data['order_type']
            data.front_text = form.cleaned_data['front_text']
            data.back_text = form.cleaned_data['back_text']
            data.color = form.cleaned_data['color']
            data.logo = form.cleaned_data['logo']
            data.description = form.cleaned_data['description']
            data.quantity = form.cleaned_data['quantity']
            data.design_image = form.cleaned_data['design_image']

            if data.order_type == "":
                messages.error(request, "Please  enter a Type")
                return redirect('customized_orders')

            if data.quantity < 15:
                messages.error(
                    request, 'We will not accept orders less than 25. Please order 25 items or more!')
                return redirect('customized_orders')
            else:
                data.save()
                messages.success(
                    request, "Successfully Placed the Order. ThanK you for ordering!")

            year = int(datetime.date.today().strftime('%Y'))
            date = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            d = datetime.date(year, month, date)
            current_date = d.strftime('%Y%m%d')

            customized_order_number = str(data.id) + current_date
            data.customized_order_number = customized_order_number
            data.save()
            return redirect('customized_orders')
        else:
            return redirect('customized_orders')
            # return redirect('home')
    return render(request, 'customized_orders/make_customized_orders.html', {})
