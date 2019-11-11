from django.urls import reverse
from django import forms
from kaucu.widgets import DatePickerInput

from django.views.generic import *
from kaucu.mixins import *
from kaucu.models import  Payment, Sale

import django_filters
from django.conf import settings


class PaymentFilter(django_filters.FilterSet):
  slug = django_filters.CharFilter(label='ID')
  paid_date = django_filters.DateFilter(input_formats=settings.DATE_INPUT_FORMATS, widget=DatePickerInput())
  class Meta:
    model = Payment
    fields = {'slug': ['exact'],'direction': ['exact'], 'method': ['contains'] }    

class PaymentForm(forms.ModelForm):
  paid_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=DatePickerInput())
  currency = forms.CharField(widget=forms.widgets.Select(attrs={'data-live-search':'true', 'data-live-search-placeholder':'Search by code'}))
  class Meta:
    model = Payment

    fields = ['direction', 'method', 'paid_date', 'currency', 'amount']

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
  ordering = '-paid_date'
  queryset = Payment.objects.prefetch()
  def get_queryset(self):
    self.filter = PaymentFilter(self.request.GET, queryset=super().get_queryset())
    return self.filter.qs

