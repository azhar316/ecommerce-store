from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Address


class IndexView(LoginRequiredMixin, generic.ListView):

    context_object_name = 'addresses'
    template_name = 'addresses/index.html'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class CreateView(LoginRequiredMixin, generic.CreateView):

    model = Address
    fields = ('name', 'nick_name', 'address_name', 'address_type',
              'line1', 'line2', 'city', 'state', 'postal_code', 'country')
    template_name = 'addresses/create.html'

    def get_success_url(self):
        return reverse('addresses:detail', args=(self.object.id,))

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user
        address.save()
        return super().form_valid(form)


class DetailView(LoginRequiredMixin, generic.DetailView):

    context_object_name = 'address'
    template_name = 'addresses/detail.html'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class UpdateView(LoginRequiredMixin, generic.UpdateView):

    fields = ('name', 'nick_name', 'address_name', 'address_type',
              'line1', 'line2', 'city', 'state', 'postal_code', 'country')
    template_name = 'addresses/update.html'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('addresses:detail', args=(self.object.id,))


class DeleteView(LoginRequiredMixin, generic.DeleteView):

    template_name = 'addresses/confirm_delete.html'
    success_url = reverse_lazy('addresses:index')

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
