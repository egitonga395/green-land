from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length = 250)
    product_id = models.IntegerField(unique=True)
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
    display_name = models.CharField(max_length = 250, default = "rose")
    addphotos = models.ImageField(upload_to="display_image/")

#items on a cart for a given individual
class Wishlist(models.Model):
    item_name = models.OneToOneField(Item, primary_key=True, on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField()
    in_cart = models.BooleanField(default=False)
    def __str__(self):
        return self.item_name

class Transport(models.Model):
    destination = models.CharField(max_length= 250)
    price = models.PositiveIntegerField()
    include_transport = models.BooleanField(default=False)
    def __str__(self):
        return self.destination