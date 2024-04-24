from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ShortenedURL
from django.http import JsonResponse

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

def logout(request):  # Rename the function to avoid conflicts
    auth.logout(request)
    return redirect('home')

@login_required(login_url='login')
def dashboard(request):
    error = None  
    if request.method == 'POST':
        original_url = request.POST.get('long_url')
        custom_short_url = request.POST.get('custom_url')
        if original_url:
            if custom_short_url:
                if ShortenedURL.objects.filter(short_url=custom_short_url).exists():
                    error = 'Custom short URL already exists'
                else:
                    shortened_url_obj = ShortenedURL(original_url=original_url, short_url=custom_short_url, user=request.user)
                    shortened_url_obj.save()
            else:
                while True:
                    short_url = ShortenedURL.generate_short_url()
                    if not ShortenedURL.objects.filter(short_url=short_url).exists():
                        break
                shortened_url_obj = ShortenedURL(original_url=original_url, short_url=short_url, user=request.user)
                shortened_url_obj.save()
        else:
            error = 'Please provide a valid long URL'
    elif 'clear_urls' in request.POST:
        ShortenedURL.objects.filter(user=request.user).delete()
    
    shortened_urls = ShortenedURL.objects.filter(user=request.user)
    return render(request, 'loginapp/dashboard.html', {'shortened_urls': shortened_urls, 'error': error})

@login_required(login_url='login')
def delete_url(request, url_id):
    url_to_delete = ShortenedURL.objects.get(id=url_id)
    if url_to_delete.user == request.user:
        url_to_delete.delete()
    return redirect('dashboard')

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


def about(request):
    return render(request, 'loginapp/about.html')

def contact(request):
    return render(request, 'loginapp/contact.html')

def features(request):
    return render(request, 'loginapp/features.html')

from django.http import JsonResponse

def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        if original_url:  
            custom_short_url = request.POST.get('custom_url')
            if custom_short_url:
                if ShortenedURL.objects.filter(short_url=custom_short_url).exists():
                    return JsonResponse({'error': 'Custom short URL already exists'})
                else:
                    short_url = custom_short_url
            else:
                while True:
                    short_url = ShortenedURL.generate_short_url()
                    if not ShortenedURL.objects.filter(short_url=short_url).exists():
                        break
            shortened_url_obj = ShortenedURL(original_url=original_url, short_url=short_url)
            shortened_url_obj.save()
            # Return only the short URL without the '/dashboard/' part
            return JsonResponse({'shortened_url': request.build_absolute_uri('/').replace('/dashboard/', '') + short_url})
        else:
            return JsonResponse({'error': 'Please provide a valid long URL'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def redirect_original(request, short_url):
    try:
        shortened_url_obj = ShortenedURL.objects.get(short_url=short_url)
        return redirect(shortened_url_obj.original_url)
    except ShortenedURL.DoesNotExist:
        return redirect('home')

def register_login(request):
    return redirect('login')  

def login_register(request):
    return redirect('register')  

@login_required(login_url='login')
def dashboard_home(request):
    return redirect('home')  

@login_required(login_url='login')
def dashboard_about(request):
    return redirect('about')  

@login_required(login_url='login')
def dashboard_contact(request):
    return redirect('contact')  

def clear_urls(request):
    ShortenedURL.objects.all().delete()
    shortened_urls = []  # Empty list of shortened URLs
    return render(request, 'dashboard.html', {'shortened_urls': shortened_urls})

from django.shortcuts import redirect, get_object_or_404
from .models import ShortenedURL

def redirect_custom(request, short_url):
    # Check if the URL exists in the database
    shortened_url_obj = get_object_or_404(ShortenedURL, short_url=short_url)
    # Redirect to the original URL
    return redirect(shortened_url_obj.original_url)

