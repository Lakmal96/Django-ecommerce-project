from django.shortcuts import render
from . models import SupplierOrder
from accounts.models import User

# Create your views here.


def supplier_order(request):

    supplier_order = SupplierOrder.objects.filter(supplier=request.user)

    context = {
        'supplier_order': supplier_order
    }

    return render(request, 'supplier/supplier_order.html', context)


def supplier_order_detail(request, id):
    supplier_order_detail = SupplierOrder.objects.filter(id=id)
    context = {
        'supplier_order_detail': supplier_order_detail
    }
    return render(request, 'supplier/supplier_order_detail.html', context)
