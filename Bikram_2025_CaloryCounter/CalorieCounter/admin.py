from django.contrib import admin
from CalorieCounter.models import *


admin.site.register([
    User,
    BasicInfoModel,
    ConsumedCalories
])
