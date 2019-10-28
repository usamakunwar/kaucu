from django.urls import reverse

from django.views.generic import *

from .sale import SaleChildCreate, SaleChildDelete
from kaucu.models import  Sale, SalePayment, Payment, PaymentAssignForm
from kaucu.mixins import *

class SalePaymentForm(PaymentAssignForm):
  class Meta:
    model = SalePayment
    fields = ['payment', 'amount']

class SalePaymentCreate(SaleChildCreate):
  template_name = 'kaucu/base/update_dialog.html'
  form_class = SalePaymentForm
  def get_success_url(self):
    kwargs = {'path':'sale:payment', 'slug':self.kwargs.get('slug')}
    return reverse('responder:redirect_slug', kwargs=kwargs)

class SalePaymentDelete(SaleChildDelete):
  model = SalePayment
  responder_redirect_kwargs = {'path':'sale:payment'}
