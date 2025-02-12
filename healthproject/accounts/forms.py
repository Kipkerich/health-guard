from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False, max_length=10)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]
