from django import forms

from expenses import models
from groups.models import GroupMember,Group



class ExpenseForm(forms.ModelForm):
    class Meta:
        fields = ("title",'cost' ,"group")
        model = models.Expense


        widgets = {
            'cost': forms.Textarea(attrs={'rows': 1, 'cols': 1}),
            "title":forms.Textarea(attrs={'rows': 1, 'cols': 1}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        # print self.fields['group'].queryset
        super(ExpenseForm,self).__init__(*args, **kwargs)

        if user is not None:
                self.fields['group'].queryset = Group.objects.filter(members=user)
