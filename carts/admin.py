from django.contrib import admin

from .models import Cart, ProductEntry


class ProductsInline(admin.StackedInline):

    model = ProductEntry
    extra = 1


class CartAdmin(admin.ModelAdmin):
    inlines = [ProductsInline]


admin.site.register(Cart, CartAdmin)
