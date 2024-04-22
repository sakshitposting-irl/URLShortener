from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ShortenedURL
from django.http import JsonResponse

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


from django.shortcuts import render
from .models import ShortenedURL


def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        print("Received original URL:", original_url)  # Debugging: print the received original URL
        if original_url:  # Check if original_url is not None or empty
            # Generate a unique short URL
            while True:
                short_url = ShortenedURL.generate_short_url()
                if not ShortenedURL.objects.filter(short_url=short_url).exists():
                    break
            # Create ShortenedURL object with original and short URLs
            shortened_url_obj = ShortenedURL(original_url=original_url, short_url=short_url)
            shortened_url_obj.save()
            # Pass the shortened URL to the template for display
            # Dynamically generate the complete URL based on your domain
            return render(request, 'loginapp/index.html', {'shortened_url': request.build_absolute_uri('/') + short_url})
    # If it's not a POST request or original_url is empty, redirect back to the homepage
    return redirect('home')

def redirect_original(request, short_url):
    try:
        shortened_url_obj = ShortenedURL.objects.get(short_url=short_url)
        # Redirect to the original URL
        return redirect(shortened_url_obj.original_url)
    except ShortenedURL.DoesNotExist:
        # Handle case where the shortened URL is not found
        return redirect('home')  # Or any other appropriate redirect
    
def register_login(request):
    return redirect('login')  # Redirect to the login page

def login_register(request):
    return redirect('register')  # Redirect to the register page

@login_required(login_url='login')
def dashboard_home(request):
    return redirect('home')  # Redirect to the dashboard page

@login_required(login_url='login')
def dashboard_about(request):
    return redirect('about')  # Redirect to the about page

@login_required(login_url='login')
def dashboard_contact(request):
    return redirect('contact')  # Redirect to the contact page

def clear_urls(request):
    if request.method == 'POST':
        ShortenedURL.objects.all().delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def dashboard(request):
    shortened_urls = ShortenedURL.objects.all()
    error = None  # Initialize error variable
    if request.method == 'POST':
        original_url = request.POST.get('long_url')
        custom_short_url = request.POST.get('custom_url')
        if original_url:
            # Check if custom URL already exists
            if custom_short_url and ShortenedURL.objects.filter(short_url=custom_short_url).exists():
                error = 'Custom short URL already exists'
            else:
                # Save the URL if it's not empty
                if original_url:
                    shortened_url_obj = ShortenedURL(original_url=original_url, short_url=custom_short_url)
                    shortened_url_obj.save()
        else:
            error = 'Please provide a valid long URL'

    return render(request, 'loginapp/dashboard.html', {'shortened_urls': shortened_urls, 'error': error})