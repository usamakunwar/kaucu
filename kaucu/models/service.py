from django.db import models
from .sale import *
from .supplier import *

class ServiceQuerySet(models.QuerySet):
  def total_cost(self, sale_id):
    return self.filter(sale_id=sale_id).values('sale_id').annotate(cost=Sum('cost')).values('cost')
    
class Service(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  last_edit = models.DateTimeField(auto_now=True)
  sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
  supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
  cost = models.DecimalField(default=0, decimal_places=2, max_digits=8)
  currency = models.CharField(max_length=3)
  currency_rate = models.DecimalField(default=1, decimal_places=2, max_digits=8)
  
  objects = ServiceQuerySet.as_manager()
  
  class Meta:
    abstract = True
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if 'update_fields' not in kwargs:
      self.sale.recalculate_cost()
  def delete(self, *args, **kwargs):
    super().delete(*args, **kwargs)
    self.sale.recalculate_cost()
