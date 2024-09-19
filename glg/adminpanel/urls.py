from django.urls import path
from . import views


app_name="adminpanel"
urlpatterns = [
    path("", views.adminpanel, name="adminpanel"),
    path("transport/", views.transport_view, name="customerview"),
    path("item/", views.item_view, name = "itemview"),
    path('update/',views.updating_content,name='update'),
    path('users/', views.users_view ,name='users'),
    path('users/edit/<int:id>', views.users_edit ,name='users_edit'),
    path('users/delete/<int:id>', views.users_edit ,name='users_delete'),
    
]
