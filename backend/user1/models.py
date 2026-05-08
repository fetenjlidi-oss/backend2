from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
class User(AbstractUser):
    role=models.CharField(max_length=30,default='user',null=True)
    email=models.EmailField(unique=True,null=True)
    is_verified=models.BooleanField(default=False,null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user1_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user1_users_permissions',
        blank=True
    )    
    def __str__(self):
        return self.email 

