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
    
    

