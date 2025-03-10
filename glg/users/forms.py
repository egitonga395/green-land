from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.exceptions import ValidationError




class EmailForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=200, help_text='Required')


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name','password1', 'password2')


class SigninForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone_number","mpesa_number", ]
        
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '254701xxxx44'})) 

    # q = forms.CharField(label='search', 
    #                 widget=forms.TextInput)
    mpesa_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '254701xxxx44'})) 
    

    def clean(self):
        cleaned_data = super().clean()
        phone_number = self.cleaned_data['phone_number']
        mpesa_number = self.cleaned_data['mpesa_number']

        if len(phone_number) != 12 and len(mpesa_number) != 12:
            print("evident")
            raise ValidationError([
                ValidationError("Phone  number is invalid"), 
            ValidationError("mpesa number is invalid")])
        elif len(phone_number) != 12 or len(mpesa_number) != 12:
            if len(phone_number) != 12:
                raise ValidationError("Phone  number is invalid")
            if len(mpesa_number) != 12:
                raise ValidationError("Mpesa number is invalid")
        
        return self.cleaned_data
