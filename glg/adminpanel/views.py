from django.shortcuts import render
from shop.models import *
from blog.models import Blog
from mpesa.models import PaymentTransaction
from django.http import JsonResponse
from .forms import *
from users.models import *
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from shop.forms import Transport_edit_form
# Create your views here.
@login_required(login_url='users:signin')
@permission_required(["manage"], raise_exception=True)
def adminpanel(request):
    return render(request, "adminpanel/adminpanel.html")


# seeing the views and changing the states
@login_required(login_url='users:signin')
@permission_required(["manage"], raise_exception=True)
def order_view(request):
    context = {}
    orders = Order.objects.all().exclude(status="open")
    print(orders)
    context['orders'] = orders
    #we will have to return and render a template here
    if request.method == 'POST':
        if 'save' in request.POST:
            pk = request.POST.get('save')   
            print("&&&&&&&&&&&&&&&&&")
            order = Order.objects.get(order_number = pk)
            form = Order_status_form(request.POST, instance=order)
            form.save()
            return render (request, "adminpanel/order.html", context)

        # will replace to its own routing 
        elif 'view' in request.POST:
            pk = request.POST.get('view')
            #get info about the order
            order= Order.objects.get(order_number=pk)
            print(pk)
            del context['orders']
            context["order"] = order
            #get the buyer
            buyer = order.buyer
            print("The buyer is.....")
            print(buyer)
            buyer_details = CustomUser.objects.get(email=buyer)

            context["buyer_details"] = buyer_details
            print(buyer_details)

            #get the buyers profile
            buyers_profile = buyer_details.profile
            print(buyers_profile)
            context["buyers_profile"] = buyers_profile
            
            # get all carts tied to one item
            cart_items = order.cart_set.all()
            context["cart_items"] = cart_items

            # get the payments of the payments
            payments_for_order = PaymentTransaction.objects.all().filter(order_id=pk).order_by("-is_successful")[:3]
            context["payments_for_order"] = payments_for_order
            print("the payment orders are")
            print(payments_for_order)
            return render (request, "adminpanel/order_detailed.html", context)
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            print(pk)
            order = Order.objects.get(order_number=pk)
            form = Order_status_form(instance=order)
            context["form"] = form
            return render (request, "adminpanel/order.html", context)
    return render (request, "adminpanel/order.html", context)






@login_required(login_url='users:signin')
@permission_required(["can_do_all_transport"], raise_exception=True)
def transport_view(request):
    context = {}
    form = Transport_edit_form()
    transports = Transport.objects.all()
    print(transports)
    context['Transports'] = transports
    context['title'] = 'Home'
    if request.method == 'POST':
        if 'save' in request.POST:
            pk = request.POST.get('save')   
            if not pk:
                form = Transport_edit_form(request.POST)
            else:
                print("!!!!!!!!!!!!!!!!!!!!")
               
                transport = Transport.objects.get(destination = pk)
                form = Transport_edit_form(request.POST, instance=transport)
            form.save()
            form = Transport_edit_form()
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            print(pk)
            transport= Transport.objects.get(destination=pk)
            transport.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            print(pk)
            transport = Transport.objects.get(destination=pk)
            form = Transport_edit_form(instance=transport)

    context['form'] = form
    return render (request, "adminpanel/transport.html", context)




@login_required(login_url='users:signin')
@permission_required(["can_do_all_item"], raise_exception=True)
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
        



@login_required(login_url='users:signin')
@permission_required(["can_do_all_item"], raise_exception=True)
def blog_view(request):
    
        blogs = Blog.objects.all()
        pk=""
        context = {"blogs": blogs}
        if request.GET.get("submit"):
            
            blog_id = request.GET.get("submit")
            
            blog_to_be_modified = Blog.objects.get(id=request.GET.get("submit"))
            form1 = Blogform(instance = blog_to_be_modified)
            context["form1"] = form1
            context["blog"]=blog_to_be_modified
            # print(context.get("form1"))
            # print("________________The end of form 1__________________________ ")
            return render(request, "adminpanel/blog.html", context)
        
        elif request.GET.get("delete"):
            blog_to_be_modified = Blog.objects.get(id=request.GET.get("delete"))
            context["blog"]=blog_to_be_modified
          
            return render(request, "adminpanel/blog.html", context)
       
        elif request.GET.get("add"):
            form1 = Blogform()
            context["form1"] = form1
            return render(request, "adminpanel/blog.html", context)

        if request.method == "POST":
            if request.POST.get("new") == "blog1":
                print("finally")
                form = Blogform(request.POST, request.FILES)
                # print(form)
                if form.is_valid():
                    print("\n\n\n\n\n\n\nyes")
                    form.save()
                    return render(request, "adminpanel/blog.html", context)
                else:
                    print(form.errors.as_data())
                    print("no")
                    return render(request, "adminpanel/blog.html", context)
                return render(request, "adminpanel/blog.html", context)
            elif request.POST.get("saveform1"):
                print("____________________post________________form")
                instance_id = request.POST.get("saveform1")
                print(instance_id)
                blog_bound = Blog.objects.get(id = instance_id)
                # print(request.FILES)
                form = Blogform(request.POST, request.FILES, instance=blog_bound)
                
                # print(form)
                if form.is_valid():
                    print("\n\n\n\n\n\n\nyes")
                    form.save()
                else:
                    print(form.errors.as_data())
                    print("no")
                return render(request, "adminpanel/blog.html", context)

            
            elif request.POST.get("delete"):
                print(request.POST)
                product_id = request.POST["delete"]
                blog_to_be_deleted = Blog.objects.get(id=product_id).delete()
                return render(request, "adminpanel/blog.html", context)

    
        else:
            return render(request, "adminpanel/blog.html", context)
    
    # context = {"item": item,
    # "item_images": item_images}
    # return render(request, "adminpanel/item.html", context)

@login_required(login_url='users:signin')
@permission_required(["manage"], raise_exception=True)
def users_view(request):
    users = CustomUser.objects.all()
    form  =  UserModificationForm()

    context = {
        "users": users, 
        "form": form
    }
    return render(request, "adminpanel/users.html", context)


@login_required(login_url='users:signin')
@permission_required(["admin"], raise_exception=True)
def users_edit(request, id):
    user_info = CustomUser.objects.get(id = id )
    user_profile = user_info.profile
    employee = Group.objects.get_or_create(name="Employee")
    is_employee=user_info.groups.filter(name="Employee").exists()
    is_buyer=user_info.groups.filter(name="Buyer").exists()
    context = {
        "user_info": user_info,
        "user_profile": user_profile,
        "is_employee": is_employee,
        "is_buyer": is_buyer,
    }
        
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("promote"):
            employee_id = request.POST.get("promote")
            new_employee = CustomUser.objects.get(id = employee_id)
            group_employee = Group.objects.get(name="Employee")
            group_buyer = Group.objects.get(name="Buyer")
            new_employee .groups.remove( group_buyer)
            new_employee.groups.add(group_employee)
            return render(request, "adminpanel/user_edit.html", context)
        elif request.POST.get("demote"):
            employee_id = request.POST.get("demote")
            bye_employee = CustomUser.objects.get(id = employee_id)
            group_employee = Group.objects.get(name="Employee")
            group_buyer = Group.objects.get(name="Buyer")
            bye_employee.groups.remove(group_employee)
            bye_employee.groups.add(group_buyer)
            print(bye_employee.groups)
            return render(request, "adminpanel/user_edit.html", context)
    
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
def blog_update(request):
   
    blogs = Blog.objects.all()
   
    context = {"blogs": blogs}
    return render(request, "adminpanel/updating_blog.html", context)