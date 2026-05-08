from django.db import models
from django.contrib.auth.models import AbstractBaseUser
class Patient(AbstractBaseUser):
    password=models.CharField(max_length=128)
    email=models.EmailField(unique=True,null=True)
    first_name=models.CharField(max_length=100,null=True)
    last_name=models.CharField(max_length=100,null=True)
    age=models.IntegerField(null=True)
    weight=models.FloatField(null=True)
    height=models.FloatField(null=True)
    chronic_diseases=models.TextField(blank=True,null=True)


# Create your models here.
