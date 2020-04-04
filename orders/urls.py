from django.urls import path

from . import views


app_name = 'orders'
urlpatterns = [
    path('order', views.create_order, name='order'),
    path('list', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>', views.DetailView.as_view(), name='detail')
]