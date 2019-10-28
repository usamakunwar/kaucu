from django.db import models
from .service import *
from model_utils import Choices

class Hotel(Service):
  city = models.CharField(max_length=20)
  hotel = models.CharField(max_length=100)
  quantity = models.IntegerField(default=1)
  check_in = models.DateTimeField()
  check_out = models.DateTimeField()
  
  ROOM_TYPE = Choices(('D', 'double', 'Double'), ('T', 'triple', 'Triple'), ('Q', 'quad', 'Quad'), ('S', 'suite', 'Suite'))
  RATING = Choices(('5', '5star', '5 Star'), ('4', '4star', '4 Star'), ('3', '3Star', '3 Star'), ('A', 'apartment', 'Apartment'))
  VIEW = Choices(('C', 'city', 'City'), ('H', 'haram', 'Haram'), ('K', 'kabah', 'Kabah'))
  MEAL = Choices(('RO', 'roomonly', 'Room Only'), ('BB', 'breakfast', 'Breakfast'), ('HB', 'halfboard', 'Half Board'), ('FB', 'fullboard', 'Full Board'))
  room_type = models.CharField(max_length=1, choices=ROOM_TYPE)
  rating = models.CharField(max_length=1, choices=RATING)
  view = models.CharField(max_length=1, choices=VIEW)
  meal = models.CharField(max_length=2, choices=MEAL)

  def __str__(self):
    return u'{0}'.format(self.hotel)