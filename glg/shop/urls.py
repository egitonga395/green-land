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
    path("cart/quantity-form/<slug:order_number>/<slug:item_name>/", views.change_ItemQuantity, name="changeQuantity"),
    path("payment-process/", views.processing_payment, name="payment_process"),
    path("payment-process/<slug:order_number>/", views.is_payment_complete, name="is_payment_complete"),
    path("cart/transport-price-form/<slug:order_number>/", views.transport_bit, name="transportbit"),
    path('order_succesful/<slug:order_number>', views.order_succesful, name='order_succesful'),
    path('get_pdf/<slug:order_number>', views.get_pdf, name='get_pdf'),
     path('<slug:product_id>/',views.add_toCart,name='addtocart'),
    
]
