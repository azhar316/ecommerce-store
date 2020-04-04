# Generated by Django 2.2.10 on 2020-04-04 07:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('addresses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('tracking', models.CharField(choices=[('processing', 'processing'), ('in-transit', 'in-transit'), ('delivered', 'delivered'), ('returning', 'returning'), ('returned', 'returned')], max_length=120)),
                ('status', models.CharField(choices=[('delivered', 'delivered'), ('returned', 'returned'), ('refunded', 'refunded')], max_length=120)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('ordered_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('delivered_date', models.DateTimeField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='addresses.Address')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.Product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
