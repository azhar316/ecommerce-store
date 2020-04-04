from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class UserCreateForm(forms.ModelForm):

    full_name = forms.CharField(min_length=3, max_length=250, required=True)

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'password',)
