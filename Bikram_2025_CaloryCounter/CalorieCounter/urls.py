from django.urls import path
from CalorieCounter.views import *


urlpatterns = [
    path('', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
]
