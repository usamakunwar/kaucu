from django.urls import reverse

from django.views.generic import *
from .supplier import SupplierChildCreate
from kaucu.models import  Sale, SupplierPayment, Payment, PaymentAssignForm
from kaucu.mixins import *
from .supplier import SupplierChildDelete

class SupplierPaymentForm(PaymentAssignForm):
  class Meta:
    model = SupplierPayment
    fields = ['payment', 'amount']

class SupplierPaymentCreate(SupplierChildCreate):
  template_name = 'kaucu/base/update_dialog.html'
  form_class = SupplierPaymentForm
  def get_success_url(self):
    kwargs = {'path':'supplier:detail', 'pk':self.kwargs.get('pk')}
    return reverse('responder:redirect_pk', kwargs=kwargs)
    
class SupplierPaymentDelete(SupplierChildDelete):
  model = SupplierPayment


