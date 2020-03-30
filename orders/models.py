from django.db import models
from django.conf import settings
from django.utils import timezone

from carts.models import ProductEntry
from addresses.models import Address


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
    product_entries = models.ManyToManyField(ProductEntry)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    tracking = models.CharField(max_length=120, choices=ORDER_TRACKING_CHOICES)
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES)
    subtotal = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.pk
