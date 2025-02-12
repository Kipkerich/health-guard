from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib import messages

#Registration form view
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        
    else:
         form = RegisterForm()
    return render(request, "../templates/accounts/register.html", {"form": form})

#Login form view
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "../templates/accounts/login.html")

#Logout view
def logout_view(request):
    logout(request)
    return redirect("login")
