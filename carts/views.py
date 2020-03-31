from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from products.models import Product
from addresses.models import Address
from .models import Cart, ProductEntry


def view_cart(request):
    cart, new_cart = Cart.objects.get_or_create(request)
    return render(request, 'carts/cart.html', {'cart': cart})


def update(request):
    cart, new_cart = Cart.objects.get_or_create(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_key'))
    quantity = request.POST.get('product_quantity')
    product_entry = ProductEntry.objects.update_or_create(cart, product, quantity)
    cart.update_prices()
    return HttpResponseRedirect(reverse('carts:home'))


def delete_product_entry(request):
    cart, new_cart = Cart.objects.get_or_create(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_key'))
    product_entry = get_object_or_404(ProductEntry, cart=cart, product=product)
    ProductEntry.objects.get(pk=product_entry.pk).delete()
    cart.update_prices()
    return HttpResponseRedirect(reverse('carts:home'))


@login_required
def checkout(request):
    cart, new_cart = Cart.objects.get_or_create(request)
    print(cart.products.all())
    if len(cart.products.all()) is 0:
        return redirect("products:index")
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'carts/checkout.html', {'addresses': addresses, 'cart': cart})
