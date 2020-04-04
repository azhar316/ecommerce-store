from django.db import models
from django.conf import settings


ADDRESS_TYPES = (('HOME', 'HOME'),
                 ('OFFICE', 'OFFICE'),
                 ('OTHER', 'OTHER'))


class Address(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    nick_name = models.CharField(max_length=120, blank=True)
    address_name = models.CharField(max_length=120)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    line1 = models.CharField(max_length=120)
    line2 = models.CharField(max_length=120)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default="India")
    postal_code = models.CharField(max_length=25)

    def __str__(self):
        return self.address_name

    def get_short_address(self):
        for_name = self.name
        if self.nick_name:
            for_name = '{} ({})'.format(self.name, self.nick_name)
        return '{for_name} {line1} {city}'.format(
                for_name=for_name,
                line1=self.line1,
                city=self.city
            )

    def get_address(self):
        for_name = self.name
        if self.nick_name:
            for_name = '{} ({})'.format(self.name, self.nick_name)
        return '{for_name}\n{line1}\n{line2}\n{city}\n{state}-{postal_code}\n{country}'.format(
                for_name=for_name,
                line1=self.line1,
                line2=self.line2,
                city=self.city,
                state=self.state,
                postal_code=self.postal_code,
                country=self.country
            )
