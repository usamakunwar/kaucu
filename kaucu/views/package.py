from django.urls import reverse

from django.views.generic import *
from kaucu.mixins import *
from kaucu.models import  Package

import django_filters


class PackageFilter(django_filters.FilterSet):
  class Meta:
    model = Package
    fields = {'package': ['contains']} 
class PackageCreate(PermissionMixin, CreateView):
  model = Package
  template_name = 'kaucu/base/update.html'
  fields = ['package', 'allow_custom_services']
  def get_success_url(self):
    return reverse('package:detail', kwargs={'pk':self.object.pk})
  def form_valid(self, form):
    form.instance.creator = self.request.user
    return super().form_valid(form) 
class PackageUpdate(PermissionMixin, UpdateView):
  model = Package
  template_name = 'kaucu/base/update.html'
  fields = ['package', 'allow_custom_services']
  def get_success_url(self):
    return reverse('package:detail', kwargs=self.kwargs)
class PackageDetail(PermissionMixin, DetailView):
  model = Package
class PackageDelete(PermissionMixin, DeleteMixin, DeleteView):
  model = Package
  responder_redirect_kwargs = {'path':'package:list'}

class PackageList(PermissionMixin, FilterMixin, ListView):
  model = Package  
  def get_queryset(self):
    self.filter = PackageFilter(self.request.GET, queryset=super().get_queryset())
    return self.filter.qs