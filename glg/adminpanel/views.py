from django.shortcuts import render
from shop.models import *
from django.http import JsonResponse
from .forms import *

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
        pk=""
        # print(items)
        for item in items:
            dict1 = {}
            # print("Item:")
            # print(item)
            item_images = item.item_images_set.all()
            # print("Item_images:")
            # print(item_images)
            dict1["item"] = item  
            dict1["item_images"] = item_images
            # print(dict1)
            data_to_display.append(dict1)
        # print(data_to_display)
        context = {"data_to_display": data_to_display}
        if request.GET.get("submit"):
            # print("yeah")
            # print(request.GET.get("submit"))
            id = request.GET.get("submit")
            # print("______________________________________________________________")
            item_to_be_modified = Item.objects.get(product_id=request.GET.get("submit"))
            form1 = Itemform(instance = item_to_be_modified)
            
            # print(item_to_be_modified)
            item_to_be_modified_images =  item_to_be_modified.item_images_set.all()
            
            # print(item_to_be_modified_images)
            context["form1"] = form1
            context["item"]=item_to_be_modified
            # print(context.get("form1"))
            # print("________________The end of form 1__________________________ ")
            context["item_to_images"] = item_to_be_modified_images
            return render(request, "adminpanel/item.html", context)
        if request.GET.get("edit_image"):
            pk = request.GET.get("edit_image")
            item_image_to_modify = Item_images.objects.get(item_id=pk)
            imagesform = Itemimageform(instance=item_image_to_modify)
            context["imagesform"]=imagesform
            return render(request, "adminpanel/item.html", context)

        if request.method == "POST":
            print("____________________post________________form")
            instance_id = request.POST.get("saveform1")
            print(instance_id)
            item_bound = Item.objects.get(product_id = instance_id)
            # print(request.FILES)
            form = Itemform(request.POST, request.FILES, instance=item_bound)
            
            # print(form)
            if form.is_valid():
                print("\n\n\n\n\n\n\nyes")
                form.save()
            else:
                print(form.errors.as_data())
                print("no")
            return render(request, "adminpanel/item.html", context)
        else:
            return render(request, "adminpanel/item.html", context)
        



    
    # context = {"item": item,
    # "item_images": item_images}
    # return render(request, "adminpanel/item.html", context)

def customers_view(request):
    pass
