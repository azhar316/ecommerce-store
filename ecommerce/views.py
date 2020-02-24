
from django.shortcuts import render

from products.models import Product


def index(request):
    latest_products = Product.objects.order_by('time_stamp')[:5]
    discounted_products = Product.objects.order_by('-discount_percentage')
    products = {'latest_products': latest_products, 'discounted_products': discounted_products}
    return render(request, 'ecommerce/index.html', products)
