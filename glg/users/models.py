from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None           # Here               
    email = models.EmailField(unique=True, default=True)

    USERNAME_FIELD = 'email' # Here
    REQUIRED_FIELDS = [] # Here
    objects = CustomUserManager()


    class Meta:
        permissions = [
            ("promote", "Can change add a blog"),
            ("demote", "Can edit a blog"),
            ]


    def __str__(self):
        return self.email

class Profile(models.Model):
    owner = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    profilepicture = models.ImageField(upload_to="profile_pictures/")
    phone_number = models.IntegerField(blank=True, null=True)
    mpesa_number = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=250)
    def __str__(self):
        return f"{self.owner} ...... {self.phone_number}"