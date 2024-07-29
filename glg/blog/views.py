from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Blog
from shop.models import Item

# Create your views here.
def list_blog(request):
    blog = Blog.objects.all()
    paginator = Paginator(blog, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/blog_list.html", {"page_obj": page_obj})

def display_blog(request):
    blog = Blog.objects.get(pk=1)
    shop = Item.objects.filter(name__icontains=blog.title)
    return render(request, "blog/blog.html", context={"blog":blog,"shop":shop})