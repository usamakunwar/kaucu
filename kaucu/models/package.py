from django.db import models
from .user import User

class Package(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  last_edit = models.DateTimeField(auto_now=True)
  creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_packages')

  package = models.CharField(max_length=100)  
  allow_custom_services = models.BooleanField(default=True)

  def __str__(self):
    return u'{0}'.format(self.package)