
class FilterMixin():
  #redirect_field_name = 'redirect_to'
  paginate_by = 15
  paginate_orphans = 5
  filter = None
  ordering = '-created'   
   
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['filter'] = self.filter.form 
    #The filter params from GET need to be set in the paginate page urls (template)
    #Remove the 'page' param as it will duplicate
    filter_query = self.request.GET.copy()
    if 'page' in filter_query:
      filter_query.pop('page')
    filter_url = filter_query.urlencode()
    if filter_url != '':
      filter_url = '&'+filter_url
    context['filter_url'] = filter_url  
    return context
