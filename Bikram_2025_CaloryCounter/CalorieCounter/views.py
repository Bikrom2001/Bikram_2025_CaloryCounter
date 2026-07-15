from django.shortcuts import render, redirect
from CalorieCounter.models import *
from CalorieCounter.forms import *


def register_page(request):
    
    
    form_data = RegisterationForm()
    
    context ={
        "form_data": form_data,
        "form_title": "User Register Form",
        "form_btn": "Register"
    }
    
    return render(request, "master/base-form.html", context)







