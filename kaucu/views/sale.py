from django.urls import reverse
from kaucu.models import Sale, Sale_Payment
from kaucu.mixins import *

from .contact import *
from django.views.generic import *

import django_filters
from django import forms


class SaleForm(forms.ModelForm):
  price = forms.IntegerField(min_value=0)
  adult = forms.IntegerField(min_value=0)
  child = forms.IntegerField(min_value=0)
  infant = forms.IntegerField(min_value=0)
  user = forms.ModelChoiceField(queryset=User.objects.none(), widget=forms.widgets.Select(attrs={'data-live-search':'true', 'data-live-search-placeholder':'Search by Name or Id'}))
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['user'].empty_label = None
  class Meta:
    model = Sale
    fields = ['user','package', 'status', 'price', 'adult', 'child', 'infant']
  
class SaleFilter(django_filters.FilterSet):
  slug = django_filters.CharFilter(label='ID')
  class Meta:
    model = Sale
    fields = {'slug': ['exact'], 'status': ['exact']}    

class SaleCreate(ContactChildCreate):
  template_name = 'kaucu/base/update.html'
  form_class = SaleForm
  def get_form(self, form_class=None):
    #If slug exists we do not need to select a user when creating a sale, so delete it from fields
    #By default no queryset is provided to the user field, as its a related item. But we need it on POST 
    #To ensure the the selected user is valid
    form = super().get_form()
    if 'slug' in self.kwargs:
     del form.fields['user']
    elif self.request.method == 'POST':
     form.fields['user'].queryset = User.objects.contacts()
    return form

class SaleUpdate(ContactChildUpdate):
  template_name = 'kaucu/base/update.html'
  form_class = SaleForm
  model = Sale    
  def get_success_url(self):
    return reverse('sale:detail', kwargs=self.kwargs)
  def get_form(self, form_class=None):
    form = super().get_form()
    #Do not need user field on update, user should already be set
    del form.fields['user']
    return form
class SaleDelete(ContactChildDelete):
  model = Sale
class SaleDetail(ContactChildDetail):
  model = Sale
  queryset = Sale.objects.with_prefetch_related()
  def get_object(self):
    obj = super().get_object()
    obj.balance_sheet = obj.get_balance_sheet()
    obj.totals = obj.balance_sheet.balance_sheet_totals()
    return obj
  
class SaleList(PermissionMixin, FilterMixin, ListView):
  model = Sale
  def get_queryset(self):
    queryset = Sale.objects.restrict_creator(self.request.user).with_related().order_by(self.ordering)
    self.filter = SaleFilter(self.request.GET, queryset=queryset)
    return self.filter.qs

class SaleChildCreate(PermissionMixin, CreateView):
  def form_valid(self, form):
    ## When saving (new) assign the parent object 
    form.instance.sale = Sale.objects.get(slug=self.kwargs.get('slug'))
    return super().form_valid(form)
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    sale = Sale.objects.get(slug=self.kwargs.get('slug'))    
    breadcrumbs = []
    breadcrumbs.append((reverse('contact:list'), 'Contacts'))
    breadcrumbs.append((reverse('contact:detail', kwargs={'slug':sale.user.slug}), sale.user))
    breadcrumbs.append((reverse('sale:detail', kwargs={'slug':sale.slug}), sale))
    context['breadcrumbs'] = breadcrumbs
    return context  
  def get_success_url(self):
    return reverse('sale:detail', kwargs={'slug':self.object.sale.slug})

class SaleChildDelete(PermissionMixin, DeleteMixin, DeleteView):
  responder_redirect_kwargs = {'path':'sale:detail'}
  def get_success_url(self):
    self.responder_redirect_kwargs['slug'] = self.object.sale.slug
    return super().get_success_url()

class SaleChildUpdate(PermissionMixin, UpdateView):
  def get_success_url(self):
    return reverse('sale:detail', kwargs={'slug':self.object.sale.slug })
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    breadcrumbs = []
    breadcrumbs.append((reverse('contact:list'), 'Contacts'))
    breadcrumbs.append((reverse('contact:detail', kwargs={'slug':self.object.sale.user.slug}), self.object.sale.user))
    breadcrumbs.append((reverse('sale:detail', kwargs={'slug':self.object.sale.slug}), self.object.sale))
    context['breadcrumbs'] = breadcrumbs
    return context  