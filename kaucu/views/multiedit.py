
# class MultiEdit(View):
#   def getObject(self):
#     pk = self.kwargs.get('pk')
#     if pk is None:
#       return None
#     slug = self.kwargs.get('slug')
#     if slug is None:
#       return None
#     obj = User.objects.get(pk=pk, slug=slug)
#     if obj is None:
#       return None
#     return obj

#   def get(self, request, *args, **kwargs):
#       profile = self.getObject()
#       profileForm = ProfileForm(instance=profile)
#       userForm = UserForm(instance=profile.user if profile is not None else None)

#       context = {}
#       context['profile'] = profile
#       context['userForm'] = userForm
#       context['profileForm'] = profileForm
      
#       context['breadcrumbs'] = Helpers.breadcrumbs(request.path)
#       context['title'] = list(context['breadcrumbs'].keys())[-1]
#       return render(request, 'kaucu/profile_edit.html', context)
  
#   def post(self, request, *args, **kwargs):
#       profile = self.getObject()
#       userForm = UserForm(request.POST, instance=profile.user if profile is not None else None)
      
#       result = False

#       if userForm.is_valid():
#         user = userForm.save(commit=False)
#         user.username = user.email
#         user.save()
#         if profile is None:
#           profile = Profile()
#           profile.user = user
        
#         profileForm = ProfileForm(request.POST, instance=profile)
#         if profileForm.is_valid():
#             profileForm.save()
#             result = True
      
#       context = {}
#       context['profile'] = profile
#       context['userForm'] = userForm
#       context['profileForm'] = profileForm
#       context['result'] = result

#       context['breadcrumbs'] = Helpers.breadcrumbs(request.path)
#       context['title'] = list(context['breadcrumbs'].keys())[-1]

#       return render(request, 'kaucu/profile_edit.html', context)
