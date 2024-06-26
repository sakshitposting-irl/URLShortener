from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('register/', views.register, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('login/', views.login, name='login'),

    path('logout/', views.logout, name='logout'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('features/', views.features, name='features'),

    path('shorten_url/', views.shorten_url, name='shorten_url'),
  
    path('<str:short_url>/', views.redirect_original, name='redirect_original'),

    path('shorten_url/register/', views.register, name='register'),

    path('register/login/', views.register_login, name='register_login'),

    path('login/register/', views.login_register, name='login_register'),

    path('shorten_url/login/', views.login, name='shorten_login'),

    path('dashboard/home/', views.dashboard_home, name='dashboard_home'),

    path('dashboard/about/', views.dashboard_about, name='dashboard_about'),

    path('dashboard/contact/', views.dashboard_contact, name='dashboard_contact'),

    path('shorten_url/register/login/', views.register_login, name='register_login'),

    path('custom_short/', views.dashboard, name='custom_short'),
    
    path('clear/', views.clear_urls, name='clear_urls'),

    path('delete_url/<int:url_id>/', views.delete_url, name='delete_url'),

    path('redirect/<str:short_url>/', views.redirect_custom, name='redirect_custom'),
]
