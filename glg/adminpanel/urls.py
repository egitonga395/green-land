from django.urls import path
from . import views


app_name="adminpanel"
urlpatterns = [
    path("", views.adminpanel, name="adminpanel"),
    path("transport/", views.transport_view, name="customerview"),
    path("item/", views.item_view, name = "itemview"),
    
]
