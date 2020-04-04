from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import UserCreateForm


class UserCreateView(FormView):

    form_class = UserCreateForm
    template_name = 'accounts/sign_up.html'
    success_url = reverse_lazy('accounts:detail')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:detail')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        name = form.instance.full_name
        email = form.instance.email
        password = form.instance.password
        user = CustomUser.objects.create_user(full_name=name, email=email, password=password)
        login(self.request, user)
        return super().form_valid(form)


def log_in(request):
    if request.user.is_authenticated:
        return redirect('accounts:detail')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            error_message = 'Incorrect email or password'
            return render(request, 'accounts/log_in.html', {'message': error_message})

        login(request, user)
        return redirect('/')

    else:
        return render(request, 'accounts/log_in.html')


class UserDetailView(LoginRequiredMixin, DetailView):

    template_name = 'accounts/account_details.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


def log_out(request):
    logout(request)
    return redirect('/')
