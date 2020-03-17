from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

from .models import *
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    login = forms.CharField(label='login', max_length=120, required=False)
    password = forms.CharField(label='password', max_length=120,
                               widget=forms.PasswordInput)

class MealForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)
        self.fields['alergens'].required = False

    class Meta:
        model = Meal
        fields = ['name', 'description', 'alergens']
        widgets = {
                'alergens': forms.CheckboxSelectMultiple,
            }

class SymptomsForm(forms.ModelForm):

        class Meta:
            model = Symptom
            fields = ['name', 'description', 'strength']
