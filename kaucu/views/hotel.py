from django.urls import reverse
from django import forms
from bootstrap_datepicker_plus import DatePickerInput

from kaucu.models import Hotel, Supplier
from .sale import SaleChildCreate, SaleChildUpdate, SaleChildDelete
from django.conf import settings

class HotelForm(forms.ModelForm):
  cost = forms.IntegerField(min_value=0)
  check_in = forms.DateTimeField(input_formats=settings.DATETIME_INPUT_FORMATS, widget=DatePickerInput(format=settings.DATETIME_INPUT_FORMATS[0]))
  check_out = forms.DateTimeField(input_formats=settings.DATETIME_INPUT_FORMATS, widget=DatePickerInput(format=settings.DATETIME_INPUT_FORMATS[0]))
  hotel = forms.CharField(widget=forms.widgets.Select(attrs={'data-live-search':'true', 'data-live-search-placeholder':'Search by Hotel'}))

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if self.instance.hotel:
      self.fields['hotel'].widget.choices = [(self.instance.hotel, self.instance.hotel)]

  class Meta:
    model = Hotel
    fields = ['supplier','hotel','city', 'quantity', 'check_in', 'check_out', 'room_type', 'rating', 'view', 'meal', 'cost']

class HotelCreate(SaleChildCreate):
  template_name = 'kaucu/base/update.html'
  form_class = HotelForm
class HotelUpdate(SaleChildUpdate):
  template_name = 'kaucu/base/update.html'
  form_class = HotelForm
  model = Hotel    
class HotelDelete(SaleChildDelete):
  model = Hotel

