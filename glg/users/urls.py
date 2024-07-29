from django.urls import path
from . import views


app_name="Users"
urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("signin", views.login_view, name="signin"),
    path("signout", views.logout_view, name="signout"),

]
