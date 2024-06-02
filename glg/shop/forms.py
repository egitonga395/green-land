from django import forms
from .models import Wishlist, Transport
from django.core.exceptions import ValidationError


class User_quantities(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ["quantity"]

class Transport_form(forms.ModelForm):
    class Meta:
        model = Transport
        fields = "__all__"