from django.db import models
from django.conf import settings
from django.utils import timezone

from products.models import Product


class Cart(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    subtotal = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    created = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.user.username


class ProductEntry(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField(default=1)

    def get_price(self):
        return self.product.price * self.quantity
