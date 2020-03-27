from django.urls import path
from django.contrib.auth import logout

from . import views


app_name = 'accounts'
urlpatterns = [
    path('create/', views.UserCreateView.as_view(), name='sign_up'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', logout, name='log_out'),
    path('detail/', views.UserDetailView.as_view(), name='detail'),
]