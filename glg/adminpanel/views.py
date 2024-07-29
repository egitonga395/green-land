from django.shortcuts import render
from shop.models import *
from django.http import JsonResponse
from shop.models import Transport

# Create your views here.
def adminpanel(request):
    return render(request, "adminpanel/adminpanel.html")


def customer_view(request):
    transport = Transport.objects.all().values()
    data = {"transport": list(transport)}
    return JsonResponse(data)