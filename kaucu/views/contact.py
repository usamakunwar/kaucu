from django.urls import reverse

from kaucu.models import  User, Sale
from django.views.generic import *
from kaucu.mixins import *
from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse


import django_filters
from django_filters import OrderingFilter

class ContactFilter(django_filters.FilterSet):
  sort = OrderingFilter(fields=(('first_name', 'first_name'),('last_name', 'last_name'),),field_labels={'first_name': 'User account',})
  class Meta:
    model = User
    fields = {'email': ['contains'], 'first_name': ['contains'], 'last_name': ['contains'],'postcode': ['contains'],'slug': ['contains'],}    

class ContactCreate(PermissionMixin, CreateView):
  model = User
  template_name = 'kaucu/base/update.html'
  fields = ['email', 'first_name', 'last_name', 'address1','address2', 'county', 'city', 'postcode', 'phone', 'mobile', 'company']
  def get_success_url(self):
    return reverse('contact:detail', kwargs={'slug':self.object.slug})
  def form_valid(self, form):
    form.instance.creator = self.request.user
    return super().form_valid(form) 
class ContactUpdate(PermissionMixin, UpdateView):
  model = User
  template_name = 'kaucu/base/update.html'
  fields = ['email', 'first_name', 'last_name', 'address1','address2', 'county', 'city', 'postcode', 'phone', 'mobile', 'company']
  queryset = User.objects.contacts()
  def get_success_url(self):
    return reverse('contact:detail', kwargs=self.kwargs)
class ContactDelete(PermissionMixin, DeleteMixin, DeleteView):
  model = User
  responder_redirect_kwargs = {'path':'contact:list'}
class ContactDetail(PermissionMixin, DetailView):
  model = User
  #Setting this template here, becuase model is User but we need to use contact template
  template_name = 'kaucu/contact_detail.html'
  queryset = User.objects.contact_sales()
class ContactList(PermissionMixin, FilterMixin, ListView):
  model = User  
  queryset = User.objects.contacts()
  #Setting this template here, becuase model is User but we need to use contact template
  template_name = 'kaucu/contact_list.html'
  def get_queryset(self):
    self.filter = ContactFilter(self.request.GET, queryset=super().get_queryset())
    return self.filter.qs 


class ContactSearch():
  def search(request, query):
    users = User.objects.search_contacts(query)
    return JsonResponse(list(users), safe=False)



class ContactChildUpdate(PermissionMixin, UpdateView):
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    breadcrumbs = []
    breadcrumbs.append((reverse('contact:list'), 'Contacts'))
    breadcrumbs.append((reverse('contact:detail', kwargs={'slug':self.object.user.slug}), self.object.user))
    breadcrumbs.append((reverse('sale:detail', kwargs=self.kwargs), self.object))
    context['breadcrumbs'] = breadcrumbs      
    return context 
class ContactChildDetail(PermissionMixin, DetailView):
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    breadcrumbs = []
    breadcrumbs.append((reverse('contact:list'), 'Contacts'))
    breadcrumbs.append((reverse('contact:detail', kwargs={'slug':self.object.user.slug}), self.object.user))
    context['breadcrumbs'] = breadcrumbs      
    return context  
class ContactChildCreate(PermissionMixin, CreateView):
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    slug = self.kwargs.get('slug')
    if slug is not None: 
      user = User.objects.get(slug=slug)    
      breadcrumbs = []
      breadcrumbs.append((reverse('contact:list'), 'Contacts'))
      breadcrumbs.append((reverse('contact:detail', kwargs=self.kwargs), user))
      context['breadcrumbs'] = breadcrumbs      
    return context
  def form_valid(self, form):
    ## When saving (new) assign the parent object 
    if 'slug' in self.kwargs:
      form.instance.user = User.objects.get(slug=self.kwargs.get('slug'))
    form.instance.creator = self.request.user
    return super().form_valid(form) 
  def get_success_url(self):
    #override/edit this when you create child that does not need to land back to sale_detail
    return reverse('sale:detail', kwargs={'slug':self.object.slug})

class ContactChildDelete(PermissionMixin, DeleteMixin, DeleteView):
  responder_redirect_kwargs = {'path':'contact:detail'}
  def get_success_url(self):
    self.responder_redirect_kwargs['slug'] = self.object.user.slug
    return super().get_success_url()

