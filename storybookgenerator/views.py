from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def homepage(request):
    return render(request,"storybookgenerator/homepage.html")

def book_view(request):
    return render(request, "storybookgenerator/book_view.html")

def login_view(request):
   
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('storybookgenerator:homepage')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

