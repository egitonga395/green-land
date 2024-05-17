from django.shortcuts import render, get_object_or_404, redirect
from .models import Item,  Item_images, Wishlist
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages


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








    
    