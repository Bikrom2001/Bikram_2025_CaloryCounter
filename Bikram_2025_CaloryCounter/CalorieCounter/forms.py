from django import forms
from CalorieCounter.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class RegisterationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class LoginForm(AuthenticationForm):
    pass


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = BasicInfoModel
        fields = '__all__'
        exclude = ['user', 'bmr']
        
        

class ConsumedCalorieForm(forms.ModelForm):
    
    class Meta:
        model = ConsumedCalories
        fields = '__all__'
        exclude = ['consumed_by']