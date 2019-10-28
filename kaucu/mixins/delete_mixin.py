from django.urls import reverse

class DeleteMixin():
  template_name = 'kaucu/base/object_delete.html'
  responder_redirect_kwargs = None
  def get_success_url(self):
    if 'path' in self.responder_redirect_kwargs:
      if 'slug' in self.responder_redirect_kwargs:
        return reverse('responder:redirect_slug', kwargs=self.responder_redirect_kwargs)
      elif 'pk' in self.responder_redirect_kwargs:
        return reverse('responder:redirect_pk', kwargs=self.responder_redirect_kwargs)
      else:
        return reverse('responder:redirect', kwargs=self.responder_redirect_kwargs)
    else:
      return reverse('responder:respond', kwargs=self.responder_redirect_kwargs)


