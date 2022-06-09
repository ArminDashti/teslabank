from django.forms import ModelForm
from django import forms
from .models import transaction
from django.contrib.auth.hashers import make_password

class login_form(forms.Form):
    phone_number = forms.IntegerField()
    password = forms.CharField(max_length=20)

class create_account_form(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.IntegerField()
    password = forms.CharField(max_length=20)

class transfer_form(ModelForm):
    password = forms.CharField(max_length=20)
    class Meta:
        model = transaction
        exclude = ['created', 'from_id']