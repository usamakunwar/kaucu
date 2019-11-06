from django.urls import reverse

from django.views.generic import *
from .supplier import SupplierChildCreate
from kaucu.models import  Sale, Supplier_Payment, Payment, PaymentAssignForm
from kaucu.mixins import *
from .supplier import SupplierChildDelete

class Supplier_PaymentForm(PaymentAssignForm):
  class Meta:
    model = Supplier_Payment
    fields = ['payment', 'amount']

class Supplier_PaymentCreate(SupplierChildCreate):
  template_name = 'kaucu/base/update_dialog.html'
  form_class = Supplier_PaymentForm
  def get_success_url(self):
    kwargs = {'path':'supplier:detail', 'pk':self.kwargs.get('pk')}
    return reverse('responder:redirect_pk', kwargs=kwargs)
    
class Supplier_PaymentDelete(SupplierChildDelete):
  model = Supplier_Payment


