from django.shortcuts import render
from .models import Blog
from shop.models import Item

# Create your views here.

def display_blog(request):
    blog = Blog.objects.get(pk=1)
    shop = Item.objects.filter(name__icontains=blog.title)
    return render(request, "blog/blog.html", context={"blog":blog,"shop":shop})