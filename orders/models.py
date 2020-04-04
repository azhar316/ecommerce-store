from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone

from products.models import Product
from addresses.models import Address


class OrderManager(models.Manager):

    def create_orders_from_cart(self, cart, address):
        orders = list()
        for product_entry in cart.products.all():
            order = self.model.objects.create(user=cart.user, address=address,
                                              product=product_entry.product, quantity=product_entry.quantity,
                                              subtotal=product_entry.get_original_price(),
                                              total=product_entry.get_discounted_price(),
                                              tracking='delivered', status='delivered',
                                              delivered_date=timezone.now()+timedelta(days=2))
            orders.append(order)
        return orders


ORDER_STATUS_CHOICES = (
    ('delivered', 'delivered'),
    ('returned', 'returned'),
    ('refunded', 'refunded')
)

ORDER_TRACKING_CHOICES = (
    ('processing', 'processing'),
    ('in-transit', 'in-transit'),
    ('delivered', 'delivered'),
    ('returning', 'returning'),
    ('returned', 'returned')
)


class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    tracking = models.CharField(max_length=120, choices=ORDER_TRACKING_CHOICES)
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES)
    subtotal = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    ordered_date = models.DateTimeField(default=timezone.now)
    delivered_date = models.DateTimeField()

    objects = OrderManager()

    def __str__(self):
        return str(self.pk)
