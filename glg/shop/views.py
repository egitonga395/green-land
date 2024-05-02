from django.shortcuts import render, get_object_or_404
from .models import Item,  Item_images
from django.http import HttpResponse

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
    
    