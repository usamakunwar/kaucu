from django.urls import reverse

from kaucu.models import  User
from django.views.generic import *
from kaucu.mixins import *

import django_filters
#from django_filters import OrderingFilter
from django.views.generic.base import View
from django.shortcuts import render
from django import forms

####USER FOR STAFF ONLY#######
class UserFilter(django_filters.FilterSet):
  slug = django_filters.CharFilter(label='ID')
  #sort = OrderingFilter(fields=(('first_name', 'first_name'),('last_name', 'last_name'),),field_labels={'first_name': 'User account',})
  class Meta:
    model = User
    fields = {'slug': ['exact'], 'email': ['contains'], 'first_name': ['contains'], 'last_name': ['contains'],'postcode': ['contains']}    

class UserForm(forms.ModelForm):    
  new_password = forms.CharField(required=False, widget=forms.PasswordInput)
  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name', 'groups', 'color']


class UserCreate(AdminAccessMixin, CreateView):
  template_name = 'kaucu/base/update.html'
  form_class = UserForm
  def form_valid(self, form):
    form.instance.is_staff = True
    form.instance.creator = self.request.user
    if form.data['new_password']:
      form.instance.set_password(form.data['new_password'])
    return super().form_valid(form) 
  def get_success_url(self):
    return reverse('user:detail', kwargs={'slug':self.object.slug})
    
class UserUpdate(AdminAccessMixin, UpdateView):
  template_name = 'kaucu/base/update.html'
  form_class = UserForm
  queryset = User.objects.users()
  def form_valid(self, form):
    if form.data['new_password']:
      form.instance.set_password(form.data['new_password'])
    return super().form_valid(form)
  def get_success_url(self):
    return reverse('user:detail', kwargs=self.kwargs)

class UserDelete(AdminAccessMixin, DeleteMixin, DeleteView):
  model = User
  responder_redirect_kwargs = {'path':'user:list'}
class UserDetail(PermissionMixin, DetailView):
  model = User
  queryset = User.objects.users()
class UserList(AdminAccessMixin, FilterMixin, ListView):
  model = User  
  queryset = User.objects.users()
  def get_queryset(self):
    self.filter = UserFilter(self.request.GET, queryset=super().get_queryset())
    return self.filter.qs 

