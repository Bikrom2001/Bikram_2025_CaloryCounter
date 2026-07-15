from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
   def __str__(self):
        return f"{self.username}"
    
    

# Name, Age, Gender, Height, Weight

class BasicInfoModel(models.Model):
    
    GENDER_TYPE =[
        ("Male", "Male"),
        ("Female", "Female")
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info', null=True)
    name = models.CharField(max_length=100, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(choices=GENDER_TYPE, max_length=10, null=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    
    
    def __str__(self):
        return f"{self.name} - {self.age}"
    
    
# consumed calories (Item name, Calorie consumed)

class ConsumedCalories(models.Model):
    
    item_name = models.CharField(max_length=200, null=True)
    calorie = models.FloatField(null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    consumed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_calorie')
    
    def __str__(self):
        return f'{self.item_name} - {self.consumed_by.username}'
