from django.urls import reverse

from django.views.generic import *

from .sale import SaleChildCreate, SaleChildDelete
from kaucu.models import  Sale, Sale_Payment, Payment, PaymentAssignForm
from kaucu.mixins import *

class Sale_PaymentForm(PaymentAssignForm):
  class Meta:
    model = Sale_Payment
    fields = ['payment', 'amount']

class Sale_PaymentCreate(SaleChildCreate):
  template_name = 'kaucu/base/update_dialog.html'
  form_class = Sale_PaymentForm
  def get_success_url(self):
    kwargs = {'path':'sale:payment', 'slug':self.kwargs.get('slug')}
    return reverse('responder:redirect_slug', kwargs=kwargs)

class Sale_PaymentDelete(SaleChildDelete):
  model = Sale_Payment
  responder_redirect_kwargs = {'path':'sale:payment'}
