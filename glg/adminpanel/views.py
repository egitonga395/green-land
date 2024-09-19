from django.shortcuts import render
from shop.models import *
from django.http import JsonResponse
from .forms import *
from users.models import *

# Create your views here.
def adminpanel(request):
    return render(request, "adminpanel/adminpanel.html")


def transport_view(request):
    
    transport  = Transport.objects.all()
    context = {"transport":transport}
    return render (request, "adminpanel/transport.html", context)

def order_view(request):
    orders = Order.objects.all()
    context = {
        "orders":orders
    }
    return render(request, "adminpanel/transport.html", context)

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
        #getting the id of item to be deleted
        if request.GET.get("delete"):
            # print("yeah")
            # print(request.GET.get("submit"))
            id = request.GET.get("delete")
            # print("______________________________________________________________")
            item_to_be_modified = Item.objects.get(product_id=request.GET.get("delete"))
            context["item"]=item_to_be_modified
            # print(context.get("form1"))
            # print("________________The end of form 1__________________________ ")
            return render(request, "adminpanel/item.html", context)
        if request.GET.get("edit_image"):
            pk = request.GET.get("edit_image")
            item_image_to_modify = Item_images.objects.get(item_id=pk)
            imagesform = Itemimageform(instance=item_image_to_modify)
            context["imagesform"]=imagesform
            context["pk"]=pk
            return render(request, "adminpanel/item.html", context)
        if request.GET.get("add"):
            form1 = Itemform()
            context["form1"] = form1
            return render(request, "adminpanel/item.html", context)

        if request.GET.get("addimage"):
            imagesform = Itemimageform()
            context["imagesform"] = imagesform
            product_id = request.GET.get("addimage")
            print(product_id)
            context["product_id"] = product_id
            return render(request, "adminpanel/item.html", context)

        if request.GET.get("deleteImage"):
            # print("yeah")
            # print(request.GET.get("submit"))
            
            # print("______________________________________________________________")
            print(request.GET.get("deleteImage"))
            image_delete = Item_images.objects.filter(item_id=request.GET.get("deleteImage")).first()
            print(image_delete)
            print("yesyes\n\n")
            context["image_delete"] = image_delete
            print(context)
            # print(context.get("form1"))
            # print("________________The end of form 1__________________________ ")
            return render(request, "adminpanel/item.html", context)

        if request.method == "POST":
            if request.POST.get("new") == "item1":
                print("finally")
                form = Itemform(request.POST, request.FILES)
                # print(form)
                if form.is_valid():
                    print("\n\n\n\n\n\n\nyes")
                    form.save()
                    return render(request, "adminpanel/item.html", context)
                else:
                    print(form.errors.as_data())
                    print("no")
                    return render(request, "adminpanel/item.html", context)
                return render(request, "adminpanel/item.html", context)
            elif request.POST.get("saveform1"):
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
            elif request.POST.get("saveform2"):
                
                instance_id = request.POST.get("saveform2")
                print(instance_id)
                item_bound = Item_images.objects.get(item_id = instance_id)
                # print(request.FILES)
                form = Itemimageform(request.POST, request.FILES, instance=item_bound)
                
                # print(form)
                if form.is_valid():
                    print("\n\n\n\n\n\n\nyes")
                    form.save()
                else:
                    print(form.errors.as_data())
                    print("no")
                return render(request, "adminpanel/item.html", context)

            
            elif request.POST.get("delete"):
                print(request.POST)
                product_id = request.POST["delete"]
                item_to_be_deleted = Item.objects.get(product_id=product_id).delete()
                return render(request, "adminpanel/item.html", context)

            elif request.POST.get("newImage"):
                print("finally")
                form = Itemimageform(request.POST, request.FILES)
                # print(form)
                if form.is_valid():
                    print(request.POST)
                    print(request.FILES)
                    item_image = Item.objects.get(product_id=request.POST["newImage"])
                    image_item = Item_images.objects.create(item_image_name=item_image, display_name=request.POST["display_name"],addphotos = request.FILES["addphotos"])
                    print(image_item)
                    image_item.save()

                    print("\n\n\n\n\n\n\nyes")
                    
                    return render(request, "adminpanel/item.html", context)
                else:
                    print(form.errors.as_data())
                    print("no")
                    return render(request, "adminpanel/item.html", context)
                return render(request, "adminpanel/item.html", context)

            elif request.POST.get("delete_image"):
                print(request.POST)
                product_id = request.POST["delete_image"]
                item_to_be_deleted = image_delete = Item_images.objects.get(item_id=product_id).delete()
                return render(request, "adminpanel/item.html", context)

    
        else:
            return render(request, "adminpanel/item.html", context)
        



    
    # context = {"item": item,
    # "item_images": item_images}
    # return render(request, "adminpanel/item.html", context)


def users_view(request):
    users = CustomUser.objects.all()
    form  =  UserModificationForm()

    context = {
        "users": users, 
        "form": form
    }
    return render(request, "adminpanel/users.html", context)

def users_edit(request, id):
    user_info = CustomUser.objects.get(id = id)
    user_profile = user_info.profile
    context = {
        "user_info": user_info,
        "user_profile": user_profile
    }
    return render(request, "adminpanel/user_edit.html", context)
    



#using htmx
def updating_content(request):
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
    return render(request, "adminpanel/updating_itemhtml.html", context)