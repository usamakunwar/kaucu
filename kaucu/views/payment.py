from django.urls import reverse
from django import forms
from bootstrap_datepicker_plus import DatePickerInput

from django.views.generic import *
from kaucu.mixins import *
from kaucu.models import  Payment, Sale

import django_filters
from django_filters import OrderingFilter
from django.conf import settings

class PaymentFilter(django_filters.FilterSet):
  class Meta:
    model = Payment
    fields = {'direction': ['exact'], 'paidDate': ['contains'], 'method': ['contains'] }    

class PaymentForm(forms.ModelForm):
  paidDate = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=DatePickerInput(format=settings.DATE_INPUT_FORMATS[0]))
  currency = forms.CharField(widget=forms.widgets.Select(attrs={'data-live-search':'true', 'data-live-search-placeholder':'Search by code'}))
  class Meta:
    model = Payment
    fields = ['direction', 'method', 'paidDate', 'currency', 'amount']

class PaymentCreate(PermissionMixin, CreateView):
  model = Payment
  template_name = 'kaucu/base/update.html'
  form_class = PaymentForm
  def get_success_url(self):
    return reverse('payment:list')
  def form_valid(self, form):
    form.instance.creator = self.request.user
    return super().form_valid(form) 
class PaymentDelete(PermissionMixin, DeleteMixin, DeleteView):
  model = Payment
  responder_redirect_kwargs = {'path':'payment:list'}
class PaymentList(PermissionMixin, FilterMixin, ListView):
  model = Payment  
  def get_queryset(self):
    self.filter = PaymentFilter(self.request.GET, queryset=super().get_queryset())
    return self.filter.qs


