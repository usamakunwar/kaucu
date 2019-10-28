from django.db import models
from kaucu.helpers import *
from django.db.models import Sum, F    
from django.db.models.functions import Coalesce
from django import forms
from .user import User
from .sale import Sale
from model_utils import Choices

class PassengerQuerySet(models.QuerySet):
  pass
class Passenger(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  last_edit = models.DateTimeField(auto_now=True)
  sale = models.ForeignKey(Sale, on_delete=models.CASCADE)

  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=150)
  dob = models.DateField(null=True, blank=True)
  nationality = models.CharField(max_length=150, null=True, blank=True)
  birth_place = models.CharField(max_length=150, null=True, blank=True)
  passport_number = models.CharField(max_length=50, null=True, blank=True)
  passport_issue_country = models.CharField(max_length=100, null=True, blank=True)
  passport_expiry = models.DateField(null=True, blank=True)
  passport_issue = models.DateField(null=True, blank=True)
  contact_number = models.IntegerField(null=True, blank=True)
  
  TITLE = Choices(('Mr', 'mr', 'Mr'),('Mrs', 'mrs', 'Mrs'),('Miss', 'miss', 'Miss'),('Master', 'master', 'Master'), ('Dr', 'dr', 'Dr'))
  GENDER = Choices(('M', 'male', 'Male'),('F', 'female', 'Female'))
  title = models.CharField(max_length=6, choices=TITLE)
  gender = models.CharField(max_length=1, choices=GENDER)
  
  objects = PassengerQuerySet.as_manager()

  def __str__(self):
    return self.first_name+' '+self.last_name

