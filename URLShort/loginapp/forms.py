from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms 
from django.forms import PasswordInput, TextInput

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] 

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput()) 

class URLShortenerForm(forms.Form):
    url = forms.URLField(label='Enter your URL here', max_length=200)