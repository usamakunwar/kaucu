from django.db import models
from kaucu.helpers import *
from django.db.models import Sum, F    
from django.db.models.functions import Coalesce
from django import forms
from .user import User
from model_utils import Choices

class PaymentQuerySet(models.QuerySet):
  def prefetch(self):
    return self.prefetch_related('sale_payment_set', 'supplier_payment_set')
  def available_payments(self):
    sum_sale_payment = Sum(Coalesce('sale_payment__amount',0))
    sum_supplier_payment = Sum(Coalesce('supplier_payment__amount',0))
    query = self.prefetch_related('sale_payment_set', 'supplier_payment_set')
    query = query.annotate(sale_total=sum_sale_payment, supplier_total=sum_supplier_payment, available=F('amount')-(F('sale_total')+F('supplier_total')))
    query = query.order_by('-paid_date')
    return query


class Payment(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  last_edit = models.DateTimeField(auto_now=True)
  slug = models.SlugField(unique=True)
  creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_payments')

  currency = models.CharField(max_length=3)
  amount = models.DecimalField(default=0, decimal_places=2, max_digits=8)
  paid_date = models.DateField()
  
  DIRECTION = Choices(('IN', 'IN', 'IN'), ('OUT', 'OUT', 'OUT'))
  direction = models.CharField(max_length=5, choices=DIRECTION)
  METHOD = Choices(('Bank Transfer', 'banktransfer', 'Bank Transfer'), ('Cash', 'cash', 'Cash'), ('Cheque', 'cheque', 'Cheque'))
  method = models.CharField(max_length=20, choices=METHOD)

  available = None
  
  objects = PaymentQuerySet.as_manager()

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = "P"+str(Helpers.randomInt(5))
    super().save(*args, **kwargs)
  
  def delete(self, *args, **kwargs):
    #Update status of all sales associated with the payment
    #Get a local copy of salepayments, then delete, as we cannot update status before delete as it wont change
    local_sale_payments = list(self.sale_payment_set.all())
    super().delete(*args, **kwargs)
    for sale_payment in local_sale_payments:
      sale_payment.sale.update_status()

  
  def __str__(self):
    payment = str(self.paid_date)+' Payment '+self.slug+'  '+self.direction
    if self.available:
      payment += ' '+self.currency+' :'+str(self.available)
    return u'{0}'.format(payment)



class PaymentAssignForm(forms.ModelForm):
  amount = forms.DecimalField()
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    payment_queryset =  Payment.objects.available_payments()
    self.fields['payment'] = forms.ModelChoiceField(queryset= payment_queryset.exclude(available=0))
    if 'data' in kwargs:
      available_amount = payment_queryset.get(id=kwargs['data']['payment']).available
      self.fields['amount'] = forms.DecimalField(max_value=available_amount)
      

