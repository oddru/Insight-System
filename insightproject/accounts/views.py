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
            return redirect('home') # Return to home page
        else:
            form = UserCreationForm()
        return render(request, 'users/register.html', {'form':form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') #return to home if not
    return render(request, 'user/login.html')

def user_logout(request):
    logout(request)
    return redirect('home') #return to home if log out

def user_home(request):
    return render(request, "user/home.html")
    
    
        