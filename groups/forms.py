
from django import forms

class NameForm(forms.Form):
    entered_key = forms.CharField(label='Key  ', max_length=100,widget=forms.PasswordInput())

