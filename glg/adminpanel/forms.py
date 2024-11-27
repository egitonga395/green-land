from shop.models import *
from blog.models import Blog
from django.forms import ModelForm
from django import forms


class Itemform(ModelForm):
    class Meta:
        model = Item
        exclude = ('recent', 'product_id',)

    def __init__(self, *args, **kwargs):
        super(Itemform, self).__init__(*args, **kwargs)
        self.fields['image'].required = False


class Itemimageform(ModelForm):
    class Meta:
        model = Item_images
        exclude = ('item_image_name', 'item_id',)

        
class UserModificationForm(forms.Form):
    employee = forms.BooleanField()


class Blogform(ModelForm):
    class Meta:
        model = Blog
        exclude = ('slug', 'created',)

    def __init__(self, *args, **kwargs):
        super(Blogform, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
    
class Order_status_form(ModelForm):
    class Meta:
        model = Order
        fields = ('status', )

    # status= forms.ModelChoiceField(queryset=Transport.objects.all())
