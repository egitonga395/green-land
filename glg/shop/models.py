from django.db import models
from django.utils import timezone
from django.urls import reverse
import uuid
from users.models import CustomUser

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length = 250)
    product_id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to="product_image/")
    description = models.TextField()
    recent = models.DateTimeField(default=timezone.now)
    


    class Meta:
        ordering = ("recent",)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("shop:itemrequested",
                       args=[
                           self.recent.year,
                           self.recent.month,
                           self.recent.day,
                           self.product_id
])


class Item_images(models.Model):
    
    item_image_name = models.ForeignKey(Item, on_delete = models.CASCADE)
    item_id = models.CharField(max_length=250,primary_key=True, default=uuid.uuid4,)
    display_name = models.CharField(max_length = 250, default = "rose")
    addphotos = models.ImageField(upload_to="display_image/")

#items on a cart for a given individual

class Transport(models.Model):
    
    destination = models.CharField(max_length= 250, primary_key=True)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.destination


#using order model as a cart and for making order
#the status of the order will being a pending will be displayed in the cart

def get_default_transport():
    return Transport.objects.get(destination='nowhere')



class Order(models.Model):
    
    # order_number = models.SlugField(unique=True)
    # invoice_total = models.PositiveIntegerField()
    # destitation = models.OneToOneField(Transport, on_delete = models.SET_NULL, null=True)
    # transport_price = models.PositiveIntegerField(default=0)
    # grand_total = models.PositiveIntegerField()
    # include_transport = models.BooleanField(default=False)
    # created = models.DateTimeField(default=timezone.now)
    # completed = models.BooleanField(default = False)
    # def __str__(self):
    #     return f"Order_{self.order_number}"
    STATUS_CHOICES = [
    ("open", "OPEN"),
    ("clearing", "CLEARING"),
    ("closed", "CLOSED"),
]
    order_number = models.SlugField(unique=True, primary_key=True)
    buyer =  models.ForeignKey(CustomUser, on_delete= models.CASCADE,)
    destitation = models.ForeignKey(Transport, on_delete = models.CASCADE,  default=get_default_transport) 
    include_transport = models.BooleanField(default=False)
    invoice_total = models.PositiveIntegerField(default=0)
    transport_price = models.PositiveIntegerField(default=0)
    grand_total = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    status = models.CharField( max_length=200, choices=STATUS_CHOICES)
    def __str__(self):
        return f"Order_{self.order_number}"



# class Wishlist(models.Model):
#     item_name = models.OneToOneField(Item, primary_key=True, on_delete= models.CASCADE)
#     buyer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     in_cart = models.BooleanField(default=False)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null = True, blank=True)
#     def __str__(self):
#         return self.item_name.name
class Cart(models.Model):
    product_id = models.AutoField(primary_key=True)
    item_name = models.ForeignKey(Item,  on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    def __str__(self):
        return self.item_name.name