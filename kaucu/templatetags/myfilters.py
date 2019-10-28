from django import template

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
