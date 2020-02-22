from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

from products.utils import get_image_path


class Product(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    # max_discount_regex = RegexValidator('(\d){1, 2}', message="The discount should be lower than 100")
    # fix: the above validator is not working properly. An error is shown enter whole number while entering
    # any value.
    discount_percentage = models.IntegerField()
    time_stamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ProductGallery(models.Model):

    image = models.ImageField('product image', upload_to=get_image_path, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
