from django.shortcuts import render, redirect
from CalorieCounter.models import *
from CalorieCounter.forms import *


def register_page(request):
    
    return render(request, "master/base-form.html")







