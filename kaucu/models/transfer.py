from django.db import models
from .service import *
from model_utils import Choices

class Transfer(Service):
  from_location = models.CharField(max_length=100)
  from_time = models.DateTimeField()
  to_location = models.CharField(max_length=100)
  to_time = models.DateTimeField()
  adult = models.IntegerField(default=0)
  child = models.IntegerField(default=0)
  infant = models.IntegerField(default=0)
  
  VEHICLE = Choices(('Saloon', 'saloon', 'Saloon'), ('GMC', 'gmc', 'GMC'), ('7 Seater', 'seven', '7 seater'), ('10 Seater', 'ten', '10 seater'))
  vehicle = models.CharField(max_length=20, choices=VEHICLE)
  
  def __str__(self):
    return u'{0}'.format(self.from_location+' '+self.to_location)