from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse

register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg
    
@register.filter
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter
def maketitle(value):
  return value.replace('_', ' ').title()

@register.filter
def modulo(num, val):
    return num % val

@register.filter
def startAndEnd(currentPage, totalPages):
  breaker = 20

  if currentPage <= breaker:
    startFrom = 0
    endAt = breaker
  else:
    mod = currentPage % breaker
    if mod == 0:
      startFrom = currentPage - 1
    else:
      startFrom = currentPage - mod - 1
  endAt = startFrom + breaker + 1

  return str(startFrom) + ":" + str(endAt)

@register.filter
def makeClass(value):
  return value.lower()

@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

@register.filter(is_safe=True)
def create_button_slug(name, slug):
  return make_button(name, reverse(name+':create', kwargs={'slug':slug}))

@register.filter(is_safe=True)
def create_button_slug_disabled(name, slug):
  return make_button(name, reverse(name+':create', kwargs={'pk':pk}))

def make_button(name, create_url, enabled):
  return mark_safe("""  
  <div class="row">
    <div class="col-sm-6 mb-2 pr-sm-2">
      <a class="row p-4 list-group-item-action cursor align-items-center center bg-in
        {% if perms.kaucu.add_"""+name+""" %} 
        text-primary" href="""+create_url+"""
        {% else %}
        disabled" href="#"
        {% endif %}>
        <div class="col-sm-12">+ New """+name+"""</div>
      </a></div>
      <div class="col-md-6 mb-2">
        <div class="row p-4 align-items-center center bg-in clr-white">
          <div class="col-sm-12 pt-3 pb-2"></div>
        </div>
      </div>
  </div>
  """)
