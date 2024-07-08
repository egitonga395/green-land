from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = None           # Here               
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' # Here
    REQUIRED_FIELDS = [] # Here