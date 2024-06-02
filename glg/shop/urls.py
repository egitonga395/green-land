from django.urls import path
from . import views


app_name="shop"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("products/", views.product, name='products'),
    path('<int:year>/<int:month>/<int:day>/<slug:product_id>/',views.itemrequested,name='itemrequested'),
    path('cart/',views.display_cartitems,name='display_cart'),
    path('<slug:product_id>/',views.add_toCart,name='addtocart'),
    
]
