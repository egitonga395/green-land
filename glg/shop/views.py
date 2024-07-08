from django.shortcuts import render, get_object_or_404, redirect
from .models import Item,  Item_images, Wishlist, Transport, Order
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import User_quantities, Order_form
import random
import string


# Create your views here.

def homepage(request):
    return render(request,"shop/HOMEPAGE.HTML")

def product(request):
    Items = Item.objects.all()
    context = {"items":Items}
    return render(request,"shop/shop.html", context )



def itemrequested(request, product_id, year, month, day):

    item_requested=get_object_or_404(Item, 
                                     product_id = product_id,
                                     recent__day = day,
                                     recent__year = year,
                                     recent__month = month
                                     )
    display_images = item_requested.item_images_set.all()
    for display_image in display_images:
        print(display_image.addphotos)

    
    context = {"item": item_requested, "images": display_images}
    return render(request, "shop/product.html", context)

def add_toCart(request, product_id):

    Item_to_add = Item.objects.get(product_id = product_id)
 
    if (Wishlist.objects.filter(item_name__product_id=product_id).exists()):
        p = Wishlist.objects.get(item_name__product_id=product_id)
        p.quantity += 1
        p.save()
        messages.success(request, "One more item added")
    else:
        item = Item.objects.get(product_id = product_id)
        p = Wishlist.objects.create(item_name=item, quantity = 1)
        p.save()
        messages.success(request, "Item added to cart.")
        print(p)
        print(Item_to_add)
        print(Item_to_add.recent.year)
        print(Item_to_add.recent.month)
        print(Item_to_add.recent.day)
        print(product_id, end="*")
        print(Item_to_add.product_id, end= "succesful")
    return HttpResponseRedirect(reverse('shop:itemrequested', kwargs={'year':Item_to_add.recent.year,'month': Item_to_add.recent.month, 'day': Item_to_add.recent.day, 'product_id': product_id}))
        

def display_cartitems(request):
    cart_items = Wishlist.objects.all()
    invoice_total = 0
    forms = []
    order_include_transport  = Order_form()
    
    values = {}
    for cart_item in cart_items:
        incartvalue = cart_item.item_name
        itemtotal = incartvalue.price * cart_item.quantity
        invoice_total = invoice_total + itemtotal
        form =User_quantities(initial={"quantity":cart_item.quantity})
        forms.append(form)
    context = {"cart_items": cart_items, 
    "invoice_total": invoice_total, 
    "forms":forms,
    # "transport_form": transport_form,
    "order_include_transport":order_include_transport}
    if request.method == "POST":
        # the user can see the price of the transport
        if request.POST.get("submit") == "transport":
            print(request.POST)
            place = request.POST.get("destitation")
            
            transport_object = Transport.objects.get(destination = place)
            
            transport_price = transport_object.price
            context["transport_price"]=transport_price
            print("___________________________")
            print(transport_price)
            print("___________________________")
            order = Order.objects.filter(completed = False)
            if not order:
                obj1=Order.objects.create(order_number=order_number(), invoice_total=invoice_total, transport_price = transport_price, grand_total= invoice_total)
                print(obj1)
                for cart_item1 in cart_items:
                    cart_item1.order = obj1
                    cart_item1.save()

                print("/n/n/n/n")
                print("##########")
                print(obj1.wishlist_set.all())
                print("##########")
            
            

            else:
                print(order)
                order1, = order
                print(order1)
                modify_order_id = order1.order_number
                modify_order = Order.objects.get(order_number=modify_order_id)
                modify_order.transport_price = transport_price 
                print("********************")
                print(modify_order.transport_price)
                print("********************")
                modify_order.invoice_total = invoice_total
                modify_order.grand_total = invoice_total
                context["grand_total"]= modify_order.grand_total
                print(modify_order)
                modify_order.save()
                values = modify_order.wishlist_set.all()
                print("/n/n")
                print(cart_items)
                print("##########")
                print("fuck")
                print(values)
                print("##########")
                for cart_item1 in cart_items:
                    checklist = modify_order.wishlist_set.all()
                    if cart_item1 not in checklist:
                        cart_item1.order = modify_order
                        cart_item1.save()
                        print(f"{cart_item1} has been added to ")

                print(checklist)

            # context["transport_price"]=transport_price
            # values["transport_price"]=transport_price
            # print(context.get("transport_price"))
            return render(request, "shop/cart.html", context)
        elif request.POST.get("submit") == "cart":
            # the user can add the price of the transport
            print("*****************************")
            name = request.POST.get("submit")
            print(request.POST)
            print("*********************")
            order = Order.objects.filter(completed = False)
            if order:
                if request.POST.get("include_transport")=="on":
                    order1, =order
                    print(order1.transport_price)
                    order1.grand_total = order1.invoice_total+order1.transport_price
                    context["grand_total"]= order1.grand_total
                    print("___++++++++++++++++++___________")
                    print(order1.grand_total)
                    order1.include_transport = True
                    order1.save()
                else:
                    order1, =order
                    order1.grand_total = order1.invoice_total
                    context["grand_total"]= order1.grand_total
                    print(order1.grand_total)
                    order1.include_transport = False
                    order1.save()
            else:    
                obj1=Order.objects.create(order_number=order_number(), invoice_total=invoice_total, transport_price = 0, grand_total= invoice_total)   

            return render(request, "shop/cart.html", context)
        else:
            name = request.POST.get("submit")
            print(request.POST)
            new_quantity = request.POST.get("quantity")
            incart_item = Wishlist.objects.get(item_name__product_id=name)
            print(f"The old quantity {incart_item.quantity}")
            incart_item.quantity = new_quantity
            print(f" The new quantity {incart_item.quantity}")
            incart_item.save()
            print("___________________")
            print(incart_item.quantity)
            return render(request, "shop/cart.html", context)
            
    else:
         return render(request, "shop/cart.html", context)


def purchase_form(request):
    return render(request, "shop/purchase_form.html")









def order_number(id1 = ""):
    if len(id1) < 8:
        x = list(string.ascii_uppercase)
        list1 = []
        choice1 = str(random.randint(0,9))
        list1.append(choice1)
        choice2= randomalphabet(x)
        list1.append(choice2)
        char = random.choice(list1)
        id1 = id1 + char
        return order_number(id1=id1)
    else:
        return id1

def randomalphabet(x):
    char=x[random.randint(0, 23)]
    return char