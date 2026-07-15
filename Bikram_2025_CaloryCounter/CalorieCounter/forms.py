from django import forms
from CalorieCounter.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class RegisterationForm(UserCreationForm):
    class Meta:
        model = User,
        fields = ['username', 'email', 'password1', 'password2']