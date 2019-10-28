from django.db import models
from kaucu.api import CurrencyLayer
import datetime
from django.utils import timezone
from django.db.models import Sum, F, Aggregate, Count, OuterRef, Subquery, Value, CharField, When, DecimalField, Case, Q 
from .user import User

class SupplierQuerySet(models.QuerySet):
  def services_prefetch(self):
    return self.prefetch_related('hotel_set', 'flight_set', 'transfer_set', 'supplierpayment_set')
  def update_exchange_rates(self):
    rates = {'GBP':1}
    now = timezone.now()
    for supplier in self.all():
      if now.date() > supplier.last_edit.date():
        if supplier.currency not in rates:
          rates[supplier.currency] = CurrencyLayer().exchangeRate(supplier.currency, 'GBP')
          supplier.currency_rate = rates[supplier.currency]
        else:
          supplier.currency_rate = rates[supplier.currency]
        supplier.save()

class Supplier(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  last_edit = models.DateTimeField(auto_now=True)
  creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_suppliers')

  supplier = models.CharField(max_length=100)
  currency = models.CharField(max_length=3)
  currency_rate = models.DecimalField(default=1, decimal_places=2, max_digits=8)
  
  objects = SupplierQuerySet.as_manager()
  
  def __str__(self):
    return u'{0}'.format(self.supplier + ' ('+str(self.currency)+')')

  def balance_sheet(self):
    hotel_val = Value('Hotel', CharField())
    flight_val = Value('Flight', CharField())
    transfer_val = Value('Transfer', CharField())
    blank_val = Value('', CharField())
    zero_val = Value(0, DecimalField())
    
    payment_in = Case(When(payment__direction='IN', then='amount'), default=0)
    payment_out = Case(When(payment__direction='OUT', then='amount'), default=0)
    
    confirmed = Q(sale__status='Confirmed')
    
    payment = self.supplierpayment_set.all().values(paid_date=F('payment__paidDate'), out_payment=payment_out, in_payment=payment_in, package=blank_val, slug=F('payment__slug'), service=blank_val)
    hotels = self.hotel_set.filter(confirmed).values(paid_date=F('sale__confirmed_date'), out_payment=F('cost'), in_payment=zero_val , package=F('sale__package__package'), slug=F('sale__slug'), service=hotel_val)
    flights = self.flight_set.filter(confirmed).values(paid_date=F('sale__confirmed_date'), out_payment=F('cost'), in_payment=zero_val, package=F('sale__package__package'), slug=F('sale__slug'), service=flight_val)
    transfer = self.transfer_set.filter(confirmed).values(paid_date=F('sale__confirmed_date'), out_payment=F('cost'), in_payment=zero_val, package=F('sale__package__package'), slug=F('sale__slug'), service=transfer_val)

    return payment.union(hotels, flights, transfer).order_by('-paid_date')

