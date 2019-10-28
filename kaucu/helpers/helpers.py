from collections import OrderedDict
from random import randint
from django.urls import reverse

class Helpers:
  def unslugify(slug):
    replaceHyphens = slug.replace('-', ' ')
    return replaceHyphens.title()


  # def breadcrumbs(path):
  #   paths = list(filter(None, path.split('/')))
  #   link = ''
  #   breadcrumbs = OrderedDict()
  #   for path in paths:
  #     pretty = (path.replace('-', ' ')).replace('_', ' ').title()
  #     if pretty != 'Update' and pretty != "Success" and pretty != "Fail"  :
  #       link = link + '/' + path
  #       breadcrumbs[pretty] = link
  #   return breadcrumbs

  def randomInt(n):
      range_start = 10**(n-1)
      range_end = (10**n)-1
      return randint(range_start, range_end)


      # with open('kaucu/static/hotels.json', encoding='utf-8') as fh:
    #   context['hotellist'] = json.load(fh)