from django.urls import reverse
from django import forms
from bootstrap_datepicker_plus import DatePickerInput

from kaucu.models import Transfer
from .sale import SaleChildCreate, SaleChildUpdate, SaleChildDelete
from django.conf import settings

class TransferForm(forms.ModelForm):
  from_time = forms.DateTimeField(input_formats=settings.DATETIME_INPUT_FORMATS, widget=DatePickerInput(format=settings.DATETIME_INPUT_FORMATS[0]))
  to_time = forms.DateTimeField(input_formats=settings.DATETIME_INPUT_FORMATS, widget=DatePickerInput(format=settings.DATETIME_INPUT_FORMATS[0]))
  class Meta:
    model = Transfer
    fields = ['supplier', 'vehicle', 'from_location','from_time','to_location', 'to_time', 'adult', 'child', 'infant', 'cost']

class TransferCreate(SaleChildCreate):
  template_name = 'kaucu/base/update.html'
  form_class = TransferForm

class TransferUpdate(SaleChildUpdate):
  template_name = 'kaucu/base/update.html'
  form_class = TransferForm
  model = Transfer
  def get_success_url(self):
    return reverse('sale:detail', kwargs={'slug':self.object.sale.slug })
class TransferDelete(SaleChildDelete):
  model = Transfer

