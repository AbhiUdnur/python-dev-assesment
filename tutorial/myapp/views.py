from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Feature
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here.

def index(request):
    feature = Feature.objects.all()
    return render(request, 'index.html', {"features":feature})

def register(request):
    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email used already')
                return redirect('register')
            
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username already used')
                return redirect(register)
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request, 'password not same')
            return redirect('register')
    else:
        return render(request, 'register.html')

def counter(request):
    text = request.POST['text']
    amt = len(text.split())
    return render(request, 'counter.html', {'amt':amt})

                        


