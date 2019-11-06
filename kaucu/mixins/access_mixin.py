from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.urls import reverse
from django.shortcuts import render
from kaucu.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin





class PermissionMixin(PermissionRequiredMixin):
  def get_permission_required(self):
    name = self.request.resolver_match.namespace
    url_name = self.request.resolver_match.url_name
    #Contact is an alias for user (used in urls), so rename here for permissions 
    if name == 'contact':
      name = 'user'
    if url_name == 'update':
      return ('kaucu.change_'+name,)
    elif url_name == 'create':
      orange = ('kaucu.add_'+name,)
      print(orange)
      apple = self.request.user.has_perms(('kaucu.add_'+name,))
      print('apple')
      print(apple)
      return ('kaucu.add_'+name,)
    elif url_name == 'delete':
      return ('kaucu.delete_'+name,)
    #Keep this else without further condition, imply that all urls that are not the above
    #require 'view' permissions (including detail)
    else:
      return ('kaucu.view_'+name,)


##Subclass GroupAccessMixin and provide group name, (use it if we need to ignore object permissions)
class GroupAccessMixin(AccessMixin):
  def dispatch(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
        return self.handle_no_permission()
    self.raise_exception = True
    if request.user.groups.filter(name=self.group_name).exists() or request.user.is_superuser:
      return super(GroupAccessMixin, self).dispatch(request, *args, **kwargs)
    else:
        return self.handle_no_permission()   

class AdminAccessMixin(GroupAccessMixin):
  group_name = 'Admin'

class SalesAccessMixin(GroupAccessMixin):
  group_name = 'Sales'
