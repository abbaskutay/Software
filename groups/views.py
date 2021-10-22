from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from groups.models import Group,GroupMember
from groups import models

from forms import NameForm

from django.views.generic.edit import FormView
from django.forms.utils import flatatt
from django.shortcuts import render


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description","join_key")
    model = Group

    # def form_valid(self, form):
    #     self.object = form.save()
    #     self.object.users.add(self.request.user)
    #     return super(CreateGroup, self).form_valid(form)






class SingleGroup(generic.DetailView):

    model = Group


class ListGroups(generic.ListView):
    model = Group


    # users = model.objects.

#
# class ListMembers(generic.ListView):
#     model = GroupMember
#

    # group = GroupMember.objects.get(name='group_name')
    # users = group.user_set.all()




class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})





    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))


        g_key=group.join_key

        try:

            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))

        return super(JoinGroup,self).get(request, *args, **kwargs)



class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."

            )
        return super(LeaveGroup,self).get(request, *args, **kwargs)












# success_url = '/thanks/'

def joinhandeler(request, slug):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data['entered_key']

            o = Group.objects.get(slug=slug)

            if o.join_key != data:
                return render(request, 'groups/joinHandler.html',
                              {'slug': slug, 'form': form, 'message': 'Invalid Key, Please try Again!'})

            else:
                try:

                    GroupMember.objects.create(user=request.user, group=o)

                except IntegrityError:
                    messages.warning(request, ("Warning, already a member of {}".format(o.name)))

                else:
                    return render(request, 'groups/joinHandler.html',
                                  {'slug': slug, 'form': form, 'message': "You are now a member of the {} group.".format(o.name)})
                    # messages.success(request, "You are now a member of the {} group.".format(o.name))
            # ...
            # redirect to a new URL:

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    # return render(request, 'name.html', {'form': form})
    return render(request, 'groups/joinHandler.html', {'slug': slug, 'form': form})
