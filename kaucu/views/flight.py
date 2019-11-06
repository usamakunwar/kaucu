from django.urls import reverse
from django import forms
from bootstrap_datepicker_plus import DatePickerInput

from kaucu.models import Flight
from .sale import SaleChildCreate, SaleChildUpdate, SaleChildDelete
from django.conf import settings

class FlightForm(forms.ModelForm):
  cost = forms.IntegerField(min_value=0)
  adult = forms.IntegerField(min_value=0)
  child = forms.IntegerField(min_value=0)
  infant = forms.IntegerField(min_value=0)
  
  departure_time = forms.DateTimeField(input_formats=settings.DATETIME_INPUT_FORMATS, widget=DatePickerInput(format=settings.DATETIME_INPUT_FORMATS[0]))
  arrival_time = forms.DateTimeField(input_formats=settings.DATETIME_INPUT_FORMATS, widget=DatePickerInput(format=settings.DATETIME_INPUT_FORMATS[0]))
  departure_airport = forms.CharField(widget=forms.widgets.Select(attrs={'data-live-search':'true', 'data-live-search-placeholder':'Search by Airport Code or Name'}))
  arrival_airport = forms.CharField(widget=forms.widgets.Select(attrs={'data-live-search':'true', 'data-live-search-placeholder':'Search by Airport Code or Name'}))
  airline = forms.CharField(widget=forms.widgets.Select(attrs={'data-live-search':'true', 'data-live-search-placeholder':'Search by Airline'}))

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if self.instance.departure_airport:
      self.fields['departure_airport'].widget.choices = [(self.instance.departure_airport, self.instance.departure_airport)]
    if self.instance.arrival_airport:
      self.fields['arrival_airport'].widget.choices = [(self.instance.arrival_airport, self.instance.arrival_airport)]
    if self.instance.airline:
      self.fields['airline'].widget.choices = [(self.instance.airline, self.instance.airline)]

  class Meta:
    model = Flight
    fields = ['supplier', 'seat_class', 'flight_no','airline', 'departure_airport', 'departure_time', 'arrival_airport', 'arrival_time', 'adult', 'child', 'infant', 'cost']

class FlightCreate(SaleChildCreate):
  template_name = 'kaucu/base/update.html'
  form_class = FlightForm

class FlightUpdate(SaleChildUpdate):
  template_name = 'kaucu/base/update.html'
  form_class = FlightForm
  model = Flight
class FlightDelete(SaleChildDelete):
  model = Flight
