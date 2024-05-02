from django.urls import path
from . import views


app_name="shop"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("products/", views.product, name='products'),
    path('<int:year>/<int:month>/<int:day>/<slug:product_id>/',
 views.itemrequested,
 name='itemrequested')
]
