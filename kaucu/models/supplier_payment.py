from django.db import models
from .user import *
from .supplier import *
from .payment import *
from .payment_child import *
from django.db.models import Sum, Q

class SupplierPaymentQuerySet(models.QuerySet):
  def total_paid(self):
    total = self.aggregate(IN=Coalesce(Sum('amount', filter=Q(payment__direction='IN')),0), OUT=Coalesce(Sum('amount', filter=Q(payment__direction='OUT')),0))
    return total['IN'] - total['OUT']

class SupplierPayment(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  last_edit = models.DateTimeField(auto_now=True)

  supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
  payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
  amount = models.DecimalField(default=0, decimal_places=2, max_digits=8)
  
  objects = PaymentChildQuerySet.as_manager()
  
  def __str__(self):
    return u'{0}'.format('Supplier Payment')

