from django.contrib import admin
from .models import Item, Item_images

# Register your models here.
admin.site.register(Item_images)
class Item_imagesInline(admin.TabularInline):
    model = Item_images
    extra= 1
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("product_id", "name", "image", "price",)
    list_filter = ( "name",  "price",)
    prepopulated_fields = {"product_id":("name",)}
    inlines = [Item_imagesInline]
