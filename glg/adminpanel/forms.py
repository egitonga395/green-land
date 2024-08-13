from shop.models import *
from django.forms import ModelForm


class Itemform(ModelForm):
    class Meta:
        model = Item
        exclude = ('recent', 'product_id',)


class Itemimageform(ModelForm):
    class Meta:
        model = Item_images
        exclude = ('item_image_name', 'item_id',)
