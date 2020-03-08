from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator

from . import utils


class Product(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount_percentage = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(99)])
    time_stamp = models.DateTimeField(default=timezone.now)

    def get_discounted_price(self):
        try:
            discounted_price = Decimal(self.price) - ((Decimal(self.price) / 100) * self.discount_percentage)
        except ZeroDivisionError:
            discounted_price = self.price
        return round(discounted_price, 2)

    def __str__(self):
        return self.title


class ProductGallery(models.Model):

    image = models.ImageField('product image', upload_to=utils.get_image_path, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
