from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'loginapp/index.html')

def register(request):
    form = CreateUserForm()
 
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login') 
        
    context = {'registerform': form}

    return render(request, 'loginapp/register.html', context)


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'loginapp/dashboard.html')

def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            
    context = {'loginform': form}
    return render(request, 'loginapp/login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')

def about(request):
    return render(request, 'loginapp/about.html')

def contact(request):
    return render(request, 'loginapp/contact.html')

def features(request):
    return render(request, 'loginapp/features.html')

def shorten(request):
    return render(request, 'loginapp/shorten.html') 

from .forms import URLShortenerForm
from .models import ShortenedURL
import random
import string

def shorten(request):
    pass 