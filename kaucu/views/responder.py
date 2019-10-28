from django.views.generic.base import View
from django.urls import reverse
from django.shortcuts import render


class Responder(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'kaucu/base/responder.html', kwargs)

class ResponderRedirect(View):
  def get(self, request, *args, **kwargs):
    kwargs['responderURL'] = reverse(kwargs['path'])
    return render(request, 'kaucu/base/responder.html', kwargs)

class ResponderRedirectArgs(View):
  def get(self, request, *args, **kwargs):
    path = kwargs['path']
    del kwargs['path']
    kwargs['responderURL'] = reverse(path, kwargs=kwargs)
    return render(request, 'kaucu/base/responder.html', kwargs)

