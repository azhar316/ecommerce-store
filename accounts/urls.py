from django.urls import path

from . import views


app_name = 'accounts'
urlpatterns = [
    path('create/', views.UserCreateView.as_view(), name='sign_up'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),
    path('detail/', views.UserDetailView.as_view(), name='detail'),
]