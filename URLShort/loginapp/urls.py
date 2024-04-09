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

    path('shorten/', views.shorten, name='shorten'),
]