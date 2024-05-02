from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length = 250)
    product_id = models.SlugField(max_length=250, unique_for_date= "recent")
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
class wishlist(models.Model):
    item_id = models.CharField(primary_key=True)
    item_name = models.OneToOneField(Item)
    quantity = models.IntegerField()
    in_cart = models.BooleanField()