from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from carts.models import Cart
from addresses.models import Address
from .models import Order


@login_required
def create_order(request):
    if request.method != 'POST':
        redirect('carts:home')
    cart, new_cart = Cart.objects.get_or_create(request)
    address_pk = request.POST.get('address')
    address = Address.objects.get(pk=address_pk)
    Order.objects.create_orders_from_cart(cart, address)
    cart.clear_cart()
    return HttpResponseRedirect(reverse('orders:index'))


class IndexView(LoginRequiredMixin, generic.ListView):

    template_name = 'orders/index.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class DetailView(LoginRequiredMixin, generic.DetailView):

    template_name = 'orders/detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
