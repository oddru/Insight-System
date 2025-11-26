from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import authenticate, logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard instead of home
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard instead of home
    return render(request, 'users/login.html')

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('home')

def user_home(request):
    form = UserCreationForm()
    return render(request, "users/home.html", {'form': form})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('home')
    return render(request, "users/dashboard.html")
    
    
        