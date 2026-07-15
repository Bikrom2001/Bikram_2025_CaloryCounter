from django.shortcuts import render, redirect
from django.contrib import messages
from CalorieCounter.models import *
from CalorieCounter.forms import *


def register_page(request):
    
    if request.method == "POST":
        form_data = RegisterationForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'Registeration successfully')
            return redirect('login_page')
    
    
    form_data = RegisterationForm()
    
    context ={
        "form_data": form_data,
        "form_title": "User Register Form",
        "form_btn": "Register"
    }
    
    return render(request, "master/base-form.html", context)



def login_page(request):
    
    context ={
        "form_title": "User Login Form",
        "form_btn": "Login"
    }
    
    return render(request, "master/base-form.html", context)



