from django.urls import path
from CalorieCounter.views import *


urlpatterns = [
    path('', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),
    path('dashboard/', dashboard_page, name='dashboard_page'),
]
