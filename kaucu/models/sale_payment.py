from django.db import models
from .user import *
from .sale import *
from .payment import *
from .payment_child import *
from django.db.models import Sum, Q

class Sale_Payment(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  last_edit = models.DateTimeField(auto_now=True)
  sale = models.ForeignKey(Sale, on_delete=models.CASCADE)

  payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
  amount = models.DecimalField(default=0, decimal_places=2, max_digits=8)
  
  objects = PaymentChildQuerySet.as_manager()

  def __str__(self):
    return u'{0}'.format('Sale Payment')
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    self.sale.update_status()

  def delete(self, *args, **kwargs):
    super().delete(*args, **kwargs)
    self.sale.update_status()

