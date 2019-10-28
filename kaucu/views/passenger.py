from django.urls import reverse

from django.views.generic import *
from django import forms
from bootstrap_datepicker_plus import DatePickerInput

from .sale import SaleChildCreate, SaleChildUpdate, SaleChildDelete
from kaucu.models import Passenger
from kaucu.mixins import *
from django.conf import settings

class PassengerForm(forms.ModelForm):
  dob = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=DatePickerInput(format=settings.DATE_INPUT_FORMATS[0]))
  passport_expiry = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=DatePickerInput(format=settings.DATE_INPUT_FORMATS[0]))
  passport_issue = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=DatePickerInput(format=settings.DATE_INPUT_FORMATS[0]))

  class Meta:
    model = Passenger
    fields = ['title', 'first_name', 'last_name', 'gender', 'dob', 'nationality', 
    'birth_place', 'passport_number', 'passport_issue_country', 'passport_expiry', 'passport_issue', 'contact_number']

class PassengerCreate(SaleChildCreate):
  template_name = 'kaucu/base/update.html'
  form_class = PassengerForm
  def get_success_url(self):
    return reverse('sale:passenger', kwargs=self.kwargs)

class PassengerUpdate(SaleChildUpdate):
  template_name = 'kaucu/base/update.html'
  form_class = PassengerForm
  model = Passenger    
  def get_success_url(self):
    return reverse('sale:passenger', kwargs=self.kwargs)

class PassengerDelete(SaleChildDelete):
  model = Passenger
  def get_success_url(self):
    return reverse('sale:passenger', kwargs=self.kwargs)
