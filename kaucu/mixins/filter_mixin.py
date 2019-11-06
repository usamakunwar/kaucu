
class FilterMixin():
  #redirect_field_name = 'redirect_to'
  paginate_by = 5
  paginate_orphans = 5
  filter = None
  ordering = '-created'   
   
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['filter'] = self.filter.form   
    return context
