from django.db import models
from django.db.models import Sum, F

class PaymentChildQuerySet(models.QuerySet):
  def balance_sheet_totals(self):
    aggregate = self.aggregate(total_in=Sum('in_payment'), total_out=Sum('out_payment'))
    if aggregate['total_in'] != None:
      aggregate['balance'] = aggregate['total_in'] - aggregate['total_out']
    else: 
      aggregate['balance'] = 0
    return aggregate

#   def total_paid(self):
#     total = self.aggregate(IN=Coalesce(Sum('amount', filter=Q(payment__direction='IN')),0), OUT=Coalesce(Sum('amount', filter=Q(payment__direction='OUT')),0))
#     return total['IN'] - total['OUT']