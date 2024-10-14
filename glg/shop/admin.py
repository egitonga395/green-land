from django.contrib import admin
from .models import Item, Item_images, Cart, Transport, Order

# Register your models here.
admin.site.register(Item_images)
admin.site.register(Cart)
admin.site.register(Transport)


class Item_imagesInline(admin.TabularInline):
    model = Item_images
    extra= 1
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("product_id", "name", "image", "price",)
    list_filter = ( "name",  "price",)
    # prepopulated_fields = {"product_id":("name",)}
    inlines = [Item_imagesInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "invoice_total", "grand_total", "include_transport","created",)
    fields = ["order_number", "created",
    ("invoice_total",
    "include_transport", "grand_total",) ]
    list_filter = ("order_number", "created",)
    prepopulated_fields = {"order_number":("created",)}

