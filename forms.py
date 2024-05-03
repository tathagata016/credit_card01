from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'username')

class SubbankerForm(forms.ModelForm):
    class Meta:
        model = Subbanker
        fields = ('mobile',)

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('fullname', 'email', 'mobile', 'address', 'father', 'state', 'city', 'pincode', 'regnumber', 'occup', 'income', 'image1', 'image2',)

