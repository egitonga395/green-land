from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name','password1', 'password2')


class SigninForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


