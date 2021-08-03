from django.shortcuts import render, get_object_or_404, redirect
from . models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from store.models import Rating, ProductGallery
from orders.models import OrderProduct
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from . forms import RatingForm
from django.contrib import messages

# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True).order_by('-id')
        paginator = Paginator(products, 6)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-id')
        paginator = Paginator(products, 6)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        inside_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(
                user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None

    reviews = Rating.objects.filter(product_id=single_product.id)

    product_gallery = ProductGallery.objects.filter(
        product_id=single_product.id)

    context = {
        'single_product': single_product,
        'inside_cart': inside_cart,
        'order_product': order_product,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }

    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            products = Product.objects.order_by(
                '-created_date').filter(Q(product_name__icontains=keyword) | Q(category__category_name__icontains=keyword))
            product_count = products.count()
        else:
            products = Product.objects.filter(product_name__icontains='shirt')
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
        'keyword': keyword
    }
    return render(request, 'store/store.html', context)


def product_review(request, product_id):

    url = request.META.get('HTTP_REFERER')

    if request.method == "POST":
        try:
            ratings = Rating.objects.get(
                user__id=request.user.id, product__id=product_id)
            form = RatingForm(request.POST, instance=ratings)
            form.save()
            messages.success(request, "Successfully Updated the the review")
            return redirect(url)
        except Rating.DoesNotExist:
            form = RatingForm(request.POST)
            if form.is_valid():
                data = Rating()
                data.topic = form.cleaned_data['topic']
                data.ratings = form.cleaned_data['ratings']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user = request.user
                data.save()
                messages.success(request, "Successfully Addedd the review")
                return redirect(url)
