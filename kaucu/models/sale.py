from django.db import models
from django.db.models import Sum, F, Aggregate, Count, OuterRef, Subquery, Value, Min, Case, When

from .user import User
from .package import *
from kaucu.helpers import *
from kaucu.api import CurrencyLayer
from django.db.models.functions import Coalesce
from django.db.models import *

from model_utils import Choices
from datetime import date

class SaleQuerySet(models.QuerySet):
  def services_prefetch(self):
    return self.prefetch_related('hotel_set', 'flight_set', 'transfer_set', 'sale_payment_set')
  def child_prefetch(self):
    return self.prefetch_related('hotel_set', 'flight_set', 'transfer_set', 'sale_payment_set', 'passenger_set')

class Sale(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  last_edit = models.DateTimeField(auto_now=True)
  creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_sales')
  slug = models.SlugField(unique=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  package = models.ForeignKey(Package, on_delete=models.CASCADE)

  price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
  cost = models.DecimalField(default=0, decimal_places=2, max_digits=8)
  confirmed_date = models.DateField(null=True)
  adult = models.IntegerField(default=0)
  child = models.IntegerField(default=0)
  infant = models.IntegerField(default=0)

  STATUS = Choices(('New', 'new', 'New'),('Negotiating', 'negotiating', 'Negotiating'),
  ('Payment Pending', 'pending', 'Payment Pending'), ('Confirmed', 'confirmed', 'Confirmed'), ('Cancelled', 'cancelled', 'Cancelled'))
  status = models.CharField(max_length=20, choices=STATUS)
  
  objects = SaleQuerySet.as_manager()

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = "S"+str(Helpers.randomInt(6))
    super().save(*args, **kwargs)
  def __str__(self):
    return u'{0}'.format('Sale '+self.slug)
  
  def recalculate_cost(self):
    from kaucu.models import Hotel, Flight, Transfer, Supplier
    self.cost = 0
    service_classes = [Hotel,Flight,Transfer]
    for service_class in service_classes:
      services = service_class.objects.filter(sale=self)
      services.update(currency_rate=Subquery(Supplier.objects.filter(id=OuterRef('supplier_id')).values('currency_rate')))   ##update rate if needed
      self.cost += services.aggregate(t=Coalesce(Sum(F('cost')/F('currency_rate')),0))['t']
    self.save(update_fields=['cost'])

  def update_status(self):
    from kaucu.models import Sale_Payment
    ##Confirmed date = Date of first payment
    confirmed_date = Sale_Payment.objects.filter(sale=self).aggregate(date=Min('payment__paid_date'))['date']
    if confirmed_date:
      if self.status != self.STATUS.confirmed:
        self.status = self.STATUS.confirmed
      self.confirmed_date = confirmed_date
      self.save(update_fields=['status','confirmed_date'])
    else:
      self.status = self.STATUS.pending
      self.confirmed_date = None
      self.save(update_fields=['status','confirmed_date'])

  def get_balance_sheet(self):    
    payment_in = Case(When(payment__direction='IN', then='amount'), default=0)
    payment_out = Case(When(payment__direction='OUT', then='amount'), default=0)
    payment = self.sale_payment_set.all().values(paid_date=F('payment__paid_date'), out_payment=payment_out, in_payment=payment_in, payment_slug=F('payment__slug'), pk=F('pk'))
    return payment.order_by('-paid_date')





    # hotel_total = Hotel.objects.filter(sale=self).aggregate(t=Coalesce(Sum(F('cost')/F('currency_rate')),0))
    # flight_total = Flight.objects.filter(sale=self).aggregate(t=Coalesce(Sum(F('cost')/F('currency_rate')),0))
    # transfer_total = Transfer.objects.filter(sale=self).aggregate(t=Coalesce(Sum(F('cost')/F('currency_rate')),0))
    # self.cost = hotel_total['t'] + flight_total['t'] + transfer_total['t']
  
  # def monthly_margin_totals(self, date_labels):
  #   to_sum = Sum(F('price')-F('cost'))
  #   months = {}
  #   for date in date_labels:
  #     case = Sum(Case(When(confirmed_date__month=date.month, confirmed_date__year=date.year, then=F('price')-F('cost')), default=0))
  #     months[date.strftime('%m/%Y')] = case
  #   return self.values('creator_id').annotate(**months)