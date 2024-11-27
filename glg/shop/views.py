from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout, authenticate

from .models import Item,  Item_images, Cart, Transport, Order
from users.models import Profile
from users.forms import ProfileForm
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from .forms import User_quantities, Order_form, Transport_form
import random
import string
import requests
from mpesa.models import PaymentTransaction

from django.template import Template, Context

from rlextra.rml2pdf import rml2pdf
from io import BytesIO
from lxml import etree
import logging



# Create your views here.

def homepage(request):
    return render(request,"shop/HOMEPAGE.HTML")

def product(request):
    #check if there is a query
    query = request.GET.get("query")
    filtered = request.GET.get("filter")
    min_price = request.GET.get("lowest_price")
    max_price = request.GET.get("highest_price")
    context = {}
    if query:
        #do the complex search and order the items by render the context
        
        search = Item.objects.filter(
                Q(name__icontains=query)|
                Q(price__contains=query)|
                Q(description__icontains=query)
            ).order_by('-recent')
        context["items"]=search
        flower = 'flower' if request.GET.get("flower")== "on" else ''
        tree = 'tree' if request.GET.get("tree")== "on" else ''
        pot = 'pot' if request.GET.get("pot")== "on" else ''
        print(flower)
        print(tree)
        print(pot)
        print("___________")
        print(tree)
        if filtered == "on": 
            filtered = search.filter(Q(price__range=(min_price,max_price))&Q(description__icontains=flower) & Q(description__icontains=tree)&Q(description__icontains=pot))
            context["items"]=filtered
            print(context)
            return render(request,"shop/partial_shop.html", context)
        # when query is alone no filter
        else:
            context["items"]=search
            return render(request,"shop/shop.html", context)
    elif query == None and filtered=="on":
        flower = 'flower' if request.GET.get("Flowers")== "on" else ' '
        tree = 'tree' if request.GET.get("tree")== "on" else ' '
        pot = 'pot' if request.GET.get("pot")== "on" else ' '
        print(flower)
        print(tree)
        print(pot)
        filtered = Item.objects.filter(Q(price__range=(min_price,max_price))&Q(description__icontains=flower) & Q(description__icontains=tree)&Q(description__icontains=pot))
        context["items"]=filtered
        return render(request,"shop/partial_shop.html", context)


    else:
        Items = Item.objects.all()
        context = {"items":Items}
        return render(request,"shop/shop.html", context )
    #we want to add various search filters here 
    

   




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

@login_required(login_url='users:signin')
def add_toCart(request, product_id):
    Item_to_add = Item.objects.get(product_id = product_id)
    user = request.user
    print(user.email)
    #check that the user has an open order
    #pull items t
    #ensure that an item already in cart will be incremented
    open_order = Order.objects.filter(buyer=user).filter(status = "open").first()
    # print(open_order.exists())
    #instance where order exists
    print(open_order)

    if open_order is not None:
        print ("the order is not empty")
        cart_queryset = open_order.cart_set.all()
        if cart_queryset.count() ==0:
            print("The cart is empty")
            new_cart_item = Cart.objects.create(item_name=Item_to_add, quantity = 1, order=open_order)

        # if the item exist in the order
        #therefore just increment

        #loops through the queryset to get a cart
        print(cart_queryset)
        count = 0
        for cart_item in cart_queryset:
            #checks whether an item exists inside the cart_item
            if Item_to_add == cart_item.item_name:
                print("item")
                cart_item.quantity += 1
                cart_item.save()
                break
                messages.success(request, "One more item added")
            
            # the item does not exist hence we just add to the cart
            #first ensure that the item does not exist until all the list is over
            elif (Item_to_add != cart_item.item_name and count == (cart_queryset.count()-1)): 
                #if all items have been iterated through and there the product does not exist
                print("working on this!!")
                new_cart_item = Cart.objects.create(item_name=Item_to_add, quantity = 1, order=open_order)
                new_cart_item.save()
                messages.success(request, "Item added to cart.")

            else:
                count += 1 

        # add  a new open order in to the user
    else:
            transport = Transport.objects.get(destination = "nowhere" )
            new_order = Order.objects.create(order_number=order_number(), buyer=user, status = "open", destitation=transport)
            new_cart_item =  Cart.objects.create(item_name=Item_to_add, quantity = 1, order=new_order)   

    # check if the user has
    # else:
    #     #actually adds the item to the cart
    #     item = Item.objects.get(product_id = product_id)
    #     p = Wishlist.objects.create(item_name=item, quantity = 1)
    #     p.save()
    #     messages.success(request, "Item added to cart.")
    #     print(p)
    #     print(Item_to_add)
    #     print(Item_to_add.recent.year)
    #     print(Item_to_add.recent.month)
    #     print(Item_to_add.recent.day)
    #     print(product_id, end="*")
    #     print(Item_to_add.product_id, end= "succesful")
    return HttpResponseRedirect(reverse('shop:itemrequested', kwargs={'year':Item_to_add.recent.year,'month': Item_to_add.recent.month, 'day': Item_to_add.recent.day, 'product_id': product_id}))
        
@login_required(login_url='users:signin')
def get_data(request):
    user = request.user
    open_order = Order.objects.filter(buyer=user).filter(status = "open").first()
    print("######")
    print(open_order.order_number)
    print(request.GET)
    if open_order is not None:
        #dealing with the display of cart items only
        cart_items = open_order.cart_set.all()
        invoice_total = 0
        forms = []
        values = {}
        for cart_item in cart_items:
            incartvalue = cart_item.item_name
            itemtotal = incartvalue.price * cart_item.quantity
            invoice_total = invoice_total + itemtotal
            form =User_quantities(initial={"quantity":cart_item.quantity})
            forms.append(form)
        open_order.invoice_total = invoice_total
        #see the value stored in the database for transport destination
        print(open_order.destitation, end="**")



        grand_total = open_order.invoice_total +  open_order.transport_price
        print ("#$$$$")
        print(open_order.invoice_total )
        open_order.save()
        context = {"cart_items": cart_items, 
        "invoice_total": open_order.invoice_total, 
        "forms":forms,
        "order_number": open_order.order_number,
        "order_include_transport":Transport_form(initial={'destination': open_order.destitation}),
        "include_transport_check":Order_form(instance=open_order),
        "transport_price": open_order.transport_price,
        "grand_total": grand_total}
        
        return context
    else:
        context = {"statement": "your cart is empty"}

@login_required(login_url='users:signin')
def display_cartitems(request):
    #get the items belonging to the user in the order that is open
    
    return render(request, "shop/cart.html", get_data(request))

    #recieve the changed quantity value from the htmx form
@login_required(login_url='users:signin')
def change_ItemQuantity(request, order_number, item_name):
    print("yes")
    print(request.GET)
    order = Order.objects.get(order_number=order_number)
    item_modified = Item.objects.get(name=item_name)
    cart_item_modified = order.cart_set.all().filter(item_name=item_modified).first()
    print(cart_item_modified)
    if request.GET.get("op") == "sub":
        cart_item_modified.quantity -= 1
        cart_item_modified.save()
        print(cart_item_modified.quantity)
        return render(request, "shop/cart.html", get_data(request))

    elif request.GET.get("op") == "add":
        cart_item_modified.quantity += 1
        cart_item_modified.save()
        print(cart_item_modified.quantity)
        return render(request, "shop/cart.html", get_data(request))
    elif request.GET.get("op") == "delete":
        cart_item_modified.delete()
        return render(request, "shop/cart.html", get_data(request))

#deal with transport values without buttons
def transport_bit(request, order_number):

    order = Order.objects.get(order_number=order_number)
    #the transport  selected by the user
    transport_destination = request.GET.get("destination")
    transport_obj= Transport.objects.get(destination=transport_destination)
    order.destitation = transport_obj
    print("The user wants to have the product transport to:")
    print(order.destitation)
    price_transport = transport_obj.price
    
    context={
        "order_number": order.order_number,
        "invoice_total": order.invoice_total,
        "transport_price": price_transport,
        "order_include_transport":Transport_form(initial={'destination': order.destitation}),
        "include_transport_check":Order_form(instance=order),
    }
    #find out whether the user wants to include tranport or not
    include_transport_check = request.GET.get("include_transport")
    if include_transport_check == "on":
        # at this point only the grand price changes
        #the price of transport at this particular case changes in the order database
        order.include_transport = True
        order.transport_price = price_transport
        order.grand_total = order.invoice_total + order.transport_price
        order.save()
        print("Since transport is included, the grand total is")
        print(order.grand_total)
        #include the updated grand total in the context
        context["grand_total"]=order.grand_total
        return render(request, "shop/partial_cart_template.html", context)
        

    else:
        #at this point the area where the user wanted us to transport the product to is just a wish
        #the transport price in the database does not change
        order.include_transport = False
        order.transport_price = 0
        order.grand_total = order.invoice_total + order.transport_price
        order.save()
        #the grand total is equal to the invoice because the transport price is 0 in the database
        context["grand_total"]=order.grand_total
        print(order.grand_total)

        return render(request, "shop/partial_cart_template.html", context)

    

@login_required(login_url='users:signin')
def purchase_form_data(request):
    print(Order.objects.filter( status="open").filter(buyer=request.user))
    order = Order.objects.filter( status="open").filter(buyer=request.user).first()
    payment_details = ProfileForm()
    ordered_items = order.cart_set.all()
    context = {
        "order": order,
        "ordered_items": ordered_items,
        "payment_details": payment_details,
        "form_issuccessful": False

    }
    return context

@login_required(login_url='users:signin')
def purchase_form(request):
    print(purchase_form_data(request))
    return render(request, "shop/purchase_form.html", purchase_form_data(request))

@login_required(login_url='users:signin') 
def processing_payment(request):
    # RETURN A LOADING FORM WHICH HAS CALLED FOR THE API FOR STK PUSH
    #send a REQUEST 

    #get the information of the user

    user = request.user
    profile = Profile.objects.get(owner=user)

    payment_details = ProfileForm(request.POST, instance=profile )
    if payment_details.is_valid():
        payment_details.save()
        phone_number = request.POST.get("phone_number")
        mpesa_number =request.POST.get("mpesa_number")
        #form validation to ensure that the quality is met
        

        #this gets the user
        
        #the order
        open_order = Order.objects.filter(buyer=user).filter(status = "open").first()
        amount = open_order.grand_total
        url = "http://127.0.0.1:8000/mpesa/submit/"
        data = {
            "phone_number": "{}".format(mpesa_number),
            "amount":"{}".format(amount),
            "entity_id": "{}".format(open_order.order_number)
        }
        print(data)
        q=requests.post(url, json=data)
        print("________________________________________")
        context = purchase_form_data(request)
        context["payment_details"] = ProfileForm(request.POST)
        context["form_issuccessful"]=True
        return render(request, "shop/purchase_form.html", context)
    
    else:
        
        context = purchase_form_data(request)
        context["payment_details"]=payment_details
        context["form_issuccessful"]=False
        print(payment_details.errors.as_data())
        return render(request, "shop/purchase_form.html", context)


#checking if payment is complete
def is_payment_complete(request, order_number):
 
    completed_payment = PaymentTransaction.objects.filter(is_successful=True, order_id=order_number).first()
    order = Order.objects.get(order_number=order_number)
    context = {}
    print(completed_payment)
    if completed_payment == None:
        context["complete"] = False
        context["order"]  = order
        return render(request, "shop/proceeding_button.html", context)
    else:
        order = Order.objects.get(order_number=order_number)
        context["order"]  = order
        context["complete"] = True 
        return render(request, "shop/proceeding_button.html", context)
        
# moving over to the order success page
def order_succesful(request, order_number):
    order_number = Order.objects.get(order_number = order_number).order_number
    return render(request, "shop/ordersuccess.html", {"order_number": order_number})



import time
#from django.conf import settings

def check_session_timeout(request):
   if request.user.is_authenticated:
       last_activity = request.session.get('last_activity')
       if last_activity is not None:
           session_expiry_time = settings.SESSION_COOKIE_AGE
           current_time = time.time()
           if current_time - last_activity > session_expiry_time:
                logout(request)
                return redirect('Users:signin')
    
# def processing_payment(request):
#     pass
logger = logging.getLogger(__name__)
def get_pdf(request, order_number):

    #getting info to print on the pdf 
    order_info =  Order.objects.get(order_number = order_number)
    print(order_info)
    cart_items = Cart.objects.filter(order=order_number)
    print(cart_items)
    
    rml = getRML(order_info, cart_items) 
    parser = etree.XMLParser(recover=True)
    etree.fromstring(rml, parser)
    buf = BytesIO()
    
    #create the pdf
    buf = BytesIO()
    rml2pdf.go(rml, outputFileName=buf)
    buf.seek(0)
    pdfData = buf.read()

    #send the response
    response = HttpResponse(content_type='application/pdf')
    response.write(pdfData)
    response['Content-Disposition'] = 'attachment; filename=Receipt.pdf'
    return response

def getRML(order_info, cart_items, payment=None):
    """We used django template to write the RML, but you could use any other
    template language of your choice. 
    """
   

    # cwd = os.getcwd()  # Get the current working directory (cwd)
    # files = os.listdir(cwd)  # Get all the files in that directory
    # print("Files in %r: %s" % (cwd, files))
    t = Template(open('hello.rml').read())
    c = Context({
        "order_info": order_info,
        "cart_items":cart_items

    })
    rml = t.render(c)
    #django templates are unicode, and so need to be encoded to utf-8
    return rml.encode('utf8')

def about(request):
    return render(request,"shop/about.html")



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

