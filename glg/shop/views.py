from django.shortcuts import render, get_object_or_404, redirect
from .models import Item,  Item_images, Wishlist
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import User_quantities


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
    for cart_item in cart_items:
        incartvalue = cart_item.item_name
        itemtotal = incartvalue.price * cart_item.quantity
        invoice_total = invoice_total + itemtotal
        form =User_quantities(initial={"quantity":cart_item.quantity})
        forms.append(form)
        # print(form)

    #     print(invoice_total)
    #     print(cart_item, end="##")
    #     print(form)
    # print("\n final value")
    # print(invoice_total)
    # print("___")
    # print(form)
    # for form1 in forms:
    #     print(form1)
    context={"cart_items": cart_items, "invoice_total": invoice_total, "forms":forms}
    if request.method == "POST":
        name = request.POST.get("submit")
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