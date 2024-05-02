from django.urls import path
from . import views


app_name="blog"
urlpatterns = [
    path("", views.display_blog, name="testblog"),
]
