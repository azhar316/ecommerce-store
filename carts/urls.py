
from django.urls import path

from . import views


app_name = 'carts'

urlpatterns = [
    path('', views.view_cart, name='home'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete_product_entry, name='delete_entry'),
    path('checkout/', views.checkout, name='checkout'),
]
