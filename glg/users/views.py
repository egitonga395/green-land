from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group, Permission
from .forms import SignupForm, SigninForm

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            buyer, created = Group.objects.get_or_create(name='Buyer')
            user.groups.add(buyer)             
            return redirect('shop:homepage')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            print(user)
            print(user.is_superuser)
            if not user.is_superuser:
                print("yes")
                login(request, user)
                return redirect("shop:products")
                
            elif user.is_superuser:
                login(request, user)    
                return redirect("adminpanel:adminpanel")
                
    else:
        form = SigninForm()
    return render(request, 'users/signin.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('Users:signin')
