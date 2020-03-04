from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

from .models import *
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    login = forms.CharField(label='login', max_length=120, required=False)
    password = forms.CharField(label='password', max_length=120,
                               widget=forms.PasswordInput)

class AddMealForm(forms.Form):
        name = forms.CharField(label='name', max_length=250, required=True)
        description = forms.CharField(label='description', required=False)
        alergens = forms.MultipleChoiceField(choices=ALERGENS, widget=forms.CheckboxSelectMultiple)

