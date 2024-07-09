from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None           # Here               
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' # Here
    REQUIRED_FIELDS = [] # Here
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email

