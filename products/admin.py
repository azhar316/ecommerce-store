from django.contrib import admin

from .models import Product, ProductGallery


class ImagesInline(admin.StackedInline):
    model = ProductGallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesInline]


admin.site.register(Product, ProductAdmin)
