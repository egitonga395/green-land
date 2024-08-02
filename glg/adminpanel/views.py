from django.shortcuts import render
from shop.models import *
from django.http import JsonResponse
from shop.models import Transport, Item, Item_images

# Create your views here.
def adminpanel(request):
    return render(request, "adminpanel/adminpanel.html")


def transport_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        transport = Transport.objects.all().values()
        data = {"transport": list(transport)}
        
        return JsonResponse(data)
    else: 
        transport  = Transport.objects.all()
        context = {"transport":transport}
        return render (request, "adminpanel/transport.html", context)

def order_view(request):
    pass

def item_view(request):
    items = Item.objects.all()
    
    data_to_display = []
    print(items)
    for item in items:
        dict1 = {}
        print("Item:")
        print(item)
        item_images = item.item_images_set.all()
        print("Item_images:")
        print(item_images)
        dict1["item"] = item  
        dict1["item_images"] = item_images
        print(dict1)
        data_to_display.append(dict1)
    print(data_to_display)
    context = {"data_to_display": data_to_display}
    return render(request, "adminpanel/item.html", context)


    
    context = {"item": item,
    "item_images": item_images}
    return render(request, "adminpanel/item.html", context)

def customers_view(request):
    pass
