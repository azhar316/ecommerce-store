from django.urls import path

from . import views


app_name = 'addresses'
urlpatterns = [
    path('list', views.IndexView.as_view(), name='index'),
    path('add', views.CreateView.as_view(), name='create'),
    path('detail/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('update/<int:pk>', views.UpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.DeleteView.as_view(), name='delete'),
]
