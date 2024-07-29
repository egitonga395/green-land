from django.urls import path
from . import views


app_name="adminpanel"
urlpatterns = [
    path("", views.adminpanel, name="adminpanel"),
    path("transport/", views.customer_view, name="customerview"),
    
]
