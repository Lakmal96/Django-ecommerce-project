from django.shortcuts import render, redirect
from django.http import JsonResponse
from carts.models import CartItem
from . models import Order, Payment, OrderProduct
from . forms import OrderForm
from store.models import Product
import datetime
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body['orderID'])

    payment = Payment(
        user=request.user,
        payment_id=body['transactionID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to ordered products
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        order_product = OrderProduct()

        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = request.user.id
        order_product.product_id = item.product_id
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variations.set(product_variation)
        order_product.save()

        # Reduce quantity of sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear the cart
    CartItem.objects.filter(user=request.user).delete()

    # Order recieve email
    email_subject = "Thank you for Ordering from Kolamba Kade!"
    message = render_to_string('orders/order_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(email_subject, message, to=[to_email])
    send_email.send()

    # Send order_number and transaction id to sendData method in JsonResponse
    data = {
        'order_number': order.order_number,
        'transactionID': payment.payment_id
    }
    return JsonResponse(data)


def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    discount = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    discount = (1*total)/100
    grand_total = (total - discount)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone_number = form.cleaned_data['phone_number']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.district = form.cleaned_data['district']
            data.postal_code = form.cleaned_data['postal_code']
            data.order_total = grand_total
            data.discount = discount
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # generating order number
            year = int(datetime.date.today().strftime('%Y'))
            date = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            d = datetime.date(year, month, date)
            current_date = d.strftime('%Y%m%d')
            # concat primary key of order with this
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'grand_total': grand_total,
                'discount': discount,
            }

            return render(request, 'orders/payments.html', context)
        else:
            return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transaction_ID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transaction_ID)

        total_price = 0

        for op in ordered_products:
            total_price += op.product_price * op.quantity

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transaction_id': payment.payment_id,
            'payment': payment,
            'total_price': total_price
        }
        return render(request, 'orders/order_complete.html', context)

    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
