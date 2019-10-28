from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from kaucu.helpers import *
from django.db.models import *
from django.db.models.functions import Coalesce

from model_utils import Choices

class UserQuerySet(models.QuerySet):
  def users(self):
    return self.filter(is_staff=True)
  def contacts(self):
    return self.filter(is_staff=False)
  def search_contacts(self, query):
    query_split = query.split()
    if len(query_split) == 2:
      users = self.contacts().filter(Q(first_name__icontains=query_split[0]) | Q(last_name__icontains=query_split[1])).values('id', 'slug','first_name', 'last_name')
    elif len(query_split) == 1:
      users = self.contacts().filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(slug__istartswith=query)).values('id', 'slug','first_name', 'last_name')
    return users
  def contact_sales(self):
    return self.contacts().prefetch_related('sale_set')
  def created_sales(self):
    return self.users().prefetch_related('created_sales')
  def monthly_margins(self, date_labels):
    to_sum = F('created_sales__price')-F('created_sales__cost')
    months = {}
    for date in date_labels:
      case = Sum(Case(When(created_sales__confirmed_date__month=date.month, created_sales__confirmed_date__year=date.year, then=to_sum), default=0))
      months[date.strftime('%m-%Y')] = case
    return self.created_sales().values('id', 'first_name', 'last_name', 'color').annotate(**months)
  def monthly_margins_agg(self, date_labels):
    months = []
    for date in date_labels:
      months.append(Coalesce(Sum(date.strftime('%m-%Y')),0))
    return self.aggregate(*months)

class MyUserManager(UserManager):
  def get_queryset(self):
      return UserQuerySet(self.model, using=self._db)
  def users(self):
      return self.get_queryset().users()
  def contacts(self):
      return self.get_queryset().contacts()
  def search_contacts(self, query):
      return self.get_queryset().search_contacts(query)
  def contact_sales(self):
      return self.get_queryset().contact_sales()
  def monthly_margins(self, date_labels):
      return self.get_queryset().monthly_margins(date_labels)
  def monthly_margins_agg(self, date_labels):
      return self.get_queryset().monthly_margins_agg(date_labels)

class User(AbstractUser):
  created = models.DateTimeField(auto_now_add=True)
  last_edit = models.DateTimeField(auto_now=True)
  slug = models.SlugField(unique=True)
  email = models.EmailField(unique=True)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=150)
  address1 = models.CharField(max_length=100, null=True, blank=True)
  address2 = models.CharField(max_length=100, null=True, blank=True)
  county = models.CharField(max_length=100, null=True, blank=True) 
  city = models.CharField(max_length=100, null=True, blank=True)
  postcode = models.CharField(max_length=20, null=True, blank=True)
  phone = models.CharField(max_length=20, null=True, blank=True)
  mobile = models.CharField(max_length=20, null=True, blank=True)
  company = models.CharField(max_length=100, null=True, blank=True)
  color = models.CharField(max_length=7, null=True, blank=True)

  ROLE = Choices(('Admin', 'admin', 'Admin'),('Sales', 'sales', 'Sales'),('Accounts', 'accounts', 'Accounts'))
  role = models.CharField(max_length=20, choices=ROLE)
  
  objects = MyUserManager()
  creator = models.ForeignKey('self', on_delete=models.CASCADE, related_name='created_users', null=True)

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = "C"+str(Helpers.randomInt(6))
    self.username = self.email
    super().save(*args, **kwargs)
    
  def __str__(self):
    return u'{0}'.format(self.first_name+' '+self.last_name)




  # def monthly_margin_totals(self):
  #   to_sum = Sum(F('created_sales__price')-F('created_sales__cost'))
  #   filtered = self.created_sales()
  #   values = filtered.values(year=F('created_sales__confirmed_date__year'), month=F('created_sales__confirmed_date__month'), name=F('first_name'))
  #   return values.annotate(margin=to_sum).values('year', 'first_name', 'margin')

  # def monthly_margin_totals(self, last_number_of_months):
  #   to_sum = F('created_sales__price')-F('created_sales__cost')
  #   today = date.today()
  #   month_margin_totals = {}
  #   for i in range(0, last_number_of_months):
  #     date_to_filter = today - datedelta.datedelta(months=i)
  #     to_filter = Q(created_sales__confirmed_date__month=date_to_filter.month, created_sales__confirmed_date__year=date_to_filter.year)
  #     month_sum = Sum(to_sum, filter=to_filter)
  #     month_margin_totals[date_to_filter.strftime('%d/%m/%Y')] = month_sum
  #   apple = self.created_sales().annotate(**month_margin_totals)
  #   return apple
##**{field:reducer(field)}
    #self.created_sales().annotate(jan=)