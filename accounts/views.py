from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import authenticate , login , logout
from .forms import RegistrationForm

# Create your views here.
def Register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:logedin")
    else:
        form = RegistrationForm()
        
    return render(request , 'accounts/register.html' , {'form':form})

def logedin(request): 
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('myapp:home')
    else:
        form = AuthenticationForm()
    return render(request , 'accounts/logedin.html' , {'form':form})

def logedout(request):
    logout(request)
    return redirect("accounts:logedin")