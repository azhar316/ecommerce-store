from decimal import Decimal

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404

from products.models import Product


def transfer_products_to_users_cart(from_cart, to_cart):
    for product_entry in from_cart.products.all():
        # if the product already exist in the users cart delete that entry
        # and add the product_entry of from_cart to it
        product = to_cart.products.filter(product=product_entry.product)
        if product.count() == 1:
            product.delete()
        product_entry.cart = to_cart
        product_entry.save()
    from_cart.delete()


class CartManager(models.Manager):

    def get_or_create(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_cart = False
            cart = qs.first()
            if request.user.is_authenticated and cart.user is None:
                try:
                    # this will throw a RelatedObjectDoesNotExist exception if the user
                    # does not have a cart yet
                    transfer_products_to_users_cart(cart, request.user.cart)
                    request.session['cart_id'] = request.user.cart.id
                # handling RelatedObjectDoesNotExist exception
                except Exception:
                    cart.user = request.user
                    cart.save()
        else:
            cart = self.model.objects.create()
            request.session['cart_id'] = cart.id
            new_cart = True
        return cart, new_cart


class Cart(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    subtotal = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    created = models.DateTimeField(default=timezone.now, editable=False)

    objects = CartManager()

    def update_prices(self):
        discounted_price = 0
        original_price = 0
        for product_entry in self.products.all():
            original_price += product_entry.get_original_price()
            discounted_price += product_entry.get_discounted_price()
        self.subtotal = original_price
        self.total = discounted_price
        self.save()

    def clear_cart(self):
        self.products.all().delete()

    def __str__(self):
        try:
            # this will throw Anonymous User does not have a username exception,
            # if the user is not signed in
            name = self.user.username
        # handle the above exception
        except Exception:
            name = 'Anonymous'
        return name


class ProductEntryManager(models.Manager):

    def update_or_create(self, cart, product, quantity):
        product_entries = self.get_queryset().filter(cart=cart, product=product)
        if product_entries.count() == 1:
            product_entry = product_entries.first()
            product_entry.quantity = quantity
            product_entry.save()
        else:
            product_entry = self.model.objects.create(cart=cart, product=product, quantity=quantity)
        return product_entry


class ProductEntry(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField(default=1)

    objects = ProductEntryManager()

    def get_original_price(self):
        return self.product.price * self.quantity

    def get_discounted_price(self):
        return self.product.get_discounted_price() * self.quantity
