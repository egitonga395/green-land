from django import forms
from .models import Cart, Transport, Order
from django.core.exceptions import ValidationError


class User_quantities(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["quantity"]

class Transport_form(forms.ModelForm):
    class Meta:
        model = Transport
        exclude = ("price",)
        # destination = forms.ChoiceField(choices=Transport.destination)
#         destination = forms.CharField(
#     widget=forms.ChoiceField(choices=Transport.destination)  # Use the imported tuple directly here

# )
    # destination = form.ModelChoiceField(queryset=Transport.objects.all())
    destination= forms.ModelChoiceField(queryset=Transport.objects.all())


class Transport_edit_form(forms.ModelForm):
    class Meta:
        model = Transport
        fields = "__all__"


class Order_form(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["include_transport",]