from django.db import models
from kaucu.helpers import *
from django.db.models import Sum, F    
from django.db.models.functions import Coalesce
from django import forms
from .user import User
from model_utils import Choices

class PaymentQuerySet(models.QuerySet):
  def available_payments(self):
    sum_salepayment = Sum(Coalesce('salepayment__amount',0))
    sum_supplierpayment = Sum(Coalesce('supplierpayment__amount',0))
    query = self.prefetch_related('salepayment_set', 'supplierpayment_set')
    query = query.annotate(sale_total=sum_salepayment, supplier_total=sum_supplierpayment, available=F('amount')-(F('sale_total')+F('supplier_total')))
    query = query.order_by('-paidDate')
    return query


class Payment(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  last_edit = models.DateTimeField(auto_now=True)
  slug = models.SlugField(unique=True)
  creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_payments')

  currency = models.CharField(max_length=3)
  amount = models.DecimalField(default=0, decimal_places=2, max_digits=8)
  paidDate = models.DateField()
  
  DIRECTION = Choices(('IN', 'IN', 'IN'), ('OUT', 'OUT', 'OUT'))
  direction = models.CharField(max_length=5, choices=DIRECTION)
  METHOD = Choices(('Bank Transfer', 'banktransfer', 'Bank Transfer'), ('Cash', 'cash', 'Cash'), ('Cheque', 'cheque', 'Cheque'))
  method = models.CharField(max_length=20, choices=METHOD)
  
  objects = PaymentQuerySet.as_manager()

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = "P"+str(Helpers.randomInt(5))
    super().save(*args, **kwargs)
  
  def __str__(self):
    #Should only use with SalePayment / SupplierPayment
    return u'{0}'.format(str(self.paidDate)+' Payment '+self.slug+'  '+self.direction+' Available '+self.currency+' : '+str(self.available))


class PaymentAssignForm(forms.ModelForm):
  amount = forms.DecimalField()
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    payment_queryset =  Payment.objects.available_payments()
    self.fields['payment'] = forms.ModelChoiceField(queryset= payment_queryset.exclude(available=0))
    if 'data' in kwargs:
      available_amount = payment_queryset.get(id=kwargs['data']['payment']).available
      self.fields['amount'] = forms.DecimalField(max_value=available_amount)
      

