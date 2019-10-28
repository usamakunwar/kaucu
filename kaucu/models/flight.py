from django.db import models
from .service import *
from model_utils import Choices

class Flight(Service):
  departure_airport = models.CharField(max_length=100)
  departure_time = models.DateTimeField()
  arrival_airport = models.CharField(max_length=100)
  arrival_time = models.DateTimeField()
  adult = models.IntegerField(default=0)
  child = models.IntegerField(default=0)
  infant = models.IntegerField(default=0)
  airline = models.CharField(max_length=100)
  flight_no = models.CharField(max_length=10)

  SEAT_CLASS = Choices(('E', 'economy', 'Economy'), ('D', 'business', 'Business'), ('F', 'first', 'First'))
  seat_class = models.CharField(max_length=1, choices=SEAT_CLASS)

  def __str__(self):
    return u'{0}'.format(self.airline+' '+self.flight_no)