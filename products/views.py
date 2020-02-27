from django.shortcuts import render
from django.views import generic

from .models import Product


class IndexView(generic.ListView):

    model = Product
    template_name = 'products/index.html'


class DetailView(generic.DetailView):

    model = Product
    template_name = 'products/detail.html'
