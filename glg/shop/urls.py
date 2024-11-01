from django.urls import path
from . import views
    

app_name="shop"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('about/', views.about, name='about'),
    path("products/", views.product, name='products'),
    path('<int:year>/<int:month>/<int:day>/<slug:product_id>/',views.itemrequested,name='itemrequested'),
    path('cart/',views.display_cartitems,name='display_cart'),
    path('purchase_form/', views.purchase_form, name='purchase_form'),
    path('<slug:product_id>/',views.add_toCart,name='addtocart'),
    path("cart/quantity-form/<slug:order_number>/<slug:item_name>/", views.change_ItemQuantity, name="changeQuantity"),
    path("cart/transport-price-form/<slug:order_number>/", views.transport_bit, name="transportbit"),
    path('purchase_form/', views.purchase_form, name='purchase_form'),
    
]
