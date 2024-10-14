from django import forms
from .models import Cart, Transport, Order
from django.core.exceptions import ValidationError


class User_quantities(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["quantity"]

# class Transport_form(forms.ModelForm):
#     class Meta:
#         model = Transport
#         exclude = ("price",)
#         destination = forms.ChoiceField(choices=Transport.places)

class Order_form(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["destitation","include_transport"]