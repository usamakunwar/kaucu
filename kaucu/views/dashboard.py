from django.shortcuts import render
from django.views.generic.base import View
from django.forms.utils import ErrorList
from kaucu.models import Supplier, Sale, User

from datetime import date
import dateutil.relativedelta
from django.core.serializers.json import DjangoJSONEncoder
import json

class DivErrorList(ErrorList):
  def __str__(self):
    return self.as_divs()
  def as_divs(self):
    return '<p>'

class Dashboard(View):
    date_labels = None
    user_monthly_margins = None
    user_monthly_margins_agg = None
    today = date.today()
    def get(self, request, *args, **kwargs):
      Supplier.objects.update_all_supplier_ex_rates()
      self.date_labels = self.monthly_labels(12)
      self.user_monthly_margins = User.objects.monthly_margins(self.date_labels)
      self.user_monthly_margins_agg = self.user_monthly_margins.monthly_margins_agg(self.date_labels)
      #Chart will display (1) Total monthly margins of all users (2) Total monthly margins of each users
      chart_data = []
      margins_agg = self.create_margins_agg()
      chart_data.append(margins_agg[0])
      chart_data.extend(self.create_margins())

      response = {}
      response['chart_labels'] = json.dumps([i.strftime('%b-%y') for i in self.date_labels], cls=DjangoJSONEncoder)
      response['chart_data'] = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
      response['current_month_total'] = self.user_monthly_margins_agg[self.today.strftime('%m-%Y')+'__sum']
      response['current_month'] = self.today.strftime('%b-%y')
      response['current_year'] = self.today.strftime('%Y')
      response['current_year_total'] = margins_agg[1]

      return render(request, 'kaucu/dashboard.html',response)

    def create_margins_agg(self):
      chart_data_agg = {}
      chart_data_agg['data'] = []
      year_data = []
      for label in self.date_labels:
        value = self.user_monthly_margins_agg[label.strftime('%m-%Y')+'__sum']
        chart_data_agg['data'].append(value)
        if label.year == self.today.year:
          year_data.append(value)
      chart_data_agg['label'] = 'All'
      chart_data_agg['borderColor'] = 'rgba(0, 0, 0, 1)'
      chart_data_agg['pointBackgroundColor'] = 'rgba(0, 0, 0, 1)'
      return (chart_data_agg, sum(year_data))

    def create_margins(self):
      data = []
      for user in self.user_monthly_margins:
        user_chart_data = {}
        user_chart_data['data'] = []
        for label in self.date_labels:
          user_chart_data['data'].append(user[label.strftime('%m-%Y')])
          user_chart_data['label'] = user['first_name']+' '+user['last_name']
          user_chart_data['borderColor'] = user['color']
          user_chart_data['pointBackgroundColor'] = user['color']
          user_chart_data['total'] = 400
        data.append(user_chart_data)
      return data


    
    def monthly_labels(self, number):
      month_labels = []
      for i in range(0, number):
        month = self.today - dateutil.relativedelta.relativedelta(months=i)
        month_labels.append(month)
      return list(reversed(month_labels))

