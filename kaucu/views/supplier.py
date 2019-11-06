from django.urls import reverse
from django import forms
from bootstrap_datepicker_plus import DatePickerInput

from django.views.generic import *
from kaucu.models import  Supplier
from kaucu.mixins import *

import django_filters

class SupplierFilter(django_filters.FilterSet):
  class Meta:
    model = Supplier
    fields = {'supplier': ['contains'] }    

class SupplierForm(forms.ModelForm):
  currency = forms.CharField(widget=forms.widgets.Select(attrs={'data-live-search':'true', 'data-live-search-placeholder':'Search by code'}))
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if self.instance.currency:
      self.fields['currency'].widget.choices = [(self.instance.currency, self.instance.currency)]

  class Meta:
    model = Supplier
    fields = ['supplier', 'currency']

class SupplierCreate(PermissionMixin, CreateView):
  model = Supplier
  template_name = 'kaucu/base/update.html'
  form_class = SupplierForm
  def get_success_url(self):
    return reverse('supplier:detail', kwargs={'pk':self.object.pk})
  def form_valid(self, form):
    form.instance.creator = self.request.user
    return super().form_valid(form) 
class SupplierUpdate(PermissionMixin, UpdateView):
  model = Supplier
  template_name = 'kaucu/base/update.html'
  form_class = SupplierForm
  def get_success_url(self):
    return reverse('supplier:detail', kwargs=self.kwargs)
class SupplierDelete(PermissionMixin, DeleteMixin, DeleteView):
  model = Supplier
  responder_redirect_kwargs = {'path':'supplier:list'}

class SupplierList(PermissionMixin, FilterMixin, ListView):
  model = Supplier  
  def get(self, request, *args, **kwargs):
    Supplier.objects.update_all_supplier_ex_rates()
    return super().get(request, *args, **kwargs)
  def get_queryset(self):
    self.filter = SupplierFilter(self.request.GET, queryset=super().get_queryset())
    return self.filter.qs
class SupplierDetail(PermissionMixin, DetailView):
  model = Supplier
  queryset = Supplier.objects.services_prefetch()
  def get_object(self):
    obj = super().get_object()
    obj.balance_sheet = obj.get_balance_sheet()
    obj.totals = obj.balance_sheet.balance_sheet_totals()
    return obj

class SupplierChildCreate(PermissionMixin, CreateView):
  def form_valid(self, form):
    ## When saving (new) assign the parent object 
    form.instance.supplier = Supplier.objects.get(pk=self.kwargs.get('pk'))
    return super().form_valid(form)
    

class SupplierChildDelete(PermissionMixin, DeleteMixin, DeleteView):
  responder_redirect_kwargs = {'path':'supplier:detail'}
  def get_success_url(self):
    self.responder_redirect_kwargs['pk'] = self.object.supplier.pk
    return super().get_success_url()

