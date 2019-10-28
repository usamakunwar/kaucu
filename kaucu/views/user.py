from django.urls import reverse

from kaucu.models import  User
from django.views.generic import *
from kaucu.mixins import *

import django_filters
from django_filters import OrderingFilter


####USER FOR STAFF ONLY#######
class UserFilter(django_filters.FilterSet):
  sort = OrderingFilter(fields=(('first_name', 'first_name'),('last_name', 'last_name'),),field_labels={'first_name': 'User account',})
  class Meta:
    model = User
    fields = {'email': ['contains'], 'first_name': ['contains'], 'last_name': ['contains'],'postcode': ['contains'],'slug': ['contains'],}    

class UserCreate(AdminAccessMixin, CreateView):
  model = User
  template_name = 'kaucu/base/update.html'
  fields = ['email', 'first_name', 'last_name', 'groups', 'color']
  def form_valid(self, form):
    form.instance.is_staff = True
    form.instance.creator = self.request.user
    return super().form_valid(form) 
  def get_success_url(self):
    return reverse('user:detail', kwargs={'slug':self.object.slug})
    
class UserUpdate(AdminAccessMixin, UpdateView):
  model = User
  template_name = 'kaucu/base/update.html'
  fields = ['email', 'first_name', 'last_name', 'groups', 'color']
  queryset = User.objects.users()
  def get_success_url(self):
    return reverse('user:detail', kwargs=self.kwargs)
class UserDelete(AdminAccessMixin, DeleteMixin, DeleteView):
  model = User
  responder_redirect_kwargs = {'path':'user:list'}
class UserDetail(PermissionMixin, DetailView):
  model = User
  queryset = User.objects.users()
class UserList(PermissionMixin, FilterMixin, ListView):
  model = User  
  queryset = User.objects.users()
  def get_queryset(self):
    self.filter = UserFilter(self.request.GET, queryset=super().get_queryset())
    return self.filter.qs 