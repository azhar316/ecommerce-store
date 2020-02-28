from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404

from products.models import Product


class CartManager(models.Manager):

    def get_or_create(self, request):
        cart_id = request.sessions.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_cart = False
            cart = qs.first()
            if request.user.is_aunthenticated and cart.user is None:
                cart.user = request.user
                cart.save()
        else:
            cart = self.model.objects.new(user=request.user)
            request.sessions['cart_id'] = cart.id
            new_cart = True
        return cart, new_cart


class Cart(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    subtotal = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    created = models.DateTimeField(default=timezone.now, editable=False)

    objects = CartManager()

    def __str__(self):
        return self.user.username


class ProductEntry(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField(default=1)

    def get_price(self):
        return self.product.price * self.quantity
