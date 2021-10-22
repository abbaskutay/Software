# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy,reverse

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin
from django.http import Http404, HttpResponseRedirect

from . import forms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()





class ExpenseList(SelectRelatedMixin, generic.ListView):
    model = models.Expense
    select_related = ("user", "group")






class UserExpenses(generic.ListView):
    model = models.Expense
    template_name = "expenses/user_expense_list.html"

    def get_queryset(self):
        try:
            self.expense_user = User.objects.prefetch_related("expenses").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.expense_user.expenses.all()



    def get_context_data(self, **kwargs):
        context = super(UserExpenses,self).get_context_data(**kwargs)
        context["expense_user"] = self.expense_user
        return context





class ExpenseDetail(SelectRelatedMixin,generic.DeleteView):
    model = models.Expense
    select_related = ("user", "group")
    #
    def get_queryset(self):
        queryset = super(ExpenseDetail, self).get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )

class CreateExpense(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    form_class = forms.ExpenseForm
    # fields = ('message','group')
    model = models.Expense


    def get_form_kwargs(self):
        kwargs = super(CreateExpense,self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CreateExpense,self).form_valid(form)









class DeleteExpense(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Expense
    select_related = ("user", "group")
    success_url = reverse_lazy("expenses:all")

    def get_queryset(self):
        queryset = super(DeleteExpense,self).get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Expense Deleted")
        return super(DeleteExpense,self).delete(*args, **kwargs)


