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

class AddUserForm(forms.Form):
    login = forms.CharField(label='username', max_length=120, required=False)
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    repeat_password = forms.CharField(label='repeat password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='first_name', max_length=120)
    last_name = forms.CharField(label='last_name', max_length=120)
    email = forms.CharField(validators=[EmailValidator()])

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        print(password, repeat_password)
        if password != repeat_password:
            raise forms.ValidationError('password and repeat password must be the same')

class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(label='old password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='new password', widget=forms.PasswordInput)
    repeat_new_password = forms.CharField(label='repeat new password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        repeat_new_password = cleaned_data.get('repeat_new_password')
        print(old_password, new_password, repeat_new_password)
        if new_password != repeat_new_password:
            raise forms.ValidationError('new password and repeat new password must be the same')
        if old_password == new_password:
            raise forms.ValidationError('old password cannot be the same as the new one')
