from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from login.models import UserProfile
from login.forms import LoginForm

from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.core import serializers
# Create your views here.

def some_view(request):
    return HttpResponse("Hello World!")

def login_view(request):
    if request.user.is_authenticated():
        return HttpResponse("You are already Logged In :) ")
    
    if request.method =='POST':
        next_url = request.POST.get('next',None)
        uname = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=uname,password=password)
        if(user is not None):
            login(request,user)
            if next_url is not None:
                return redirect(next_url)
            else:
                return HttpResponse("Welcome "+uname)
        else:
            return HttpResponse("Invalid Credentials")   
    else:
        login_form = LoginForm()
        context_dict = {'form':login_form} 
        return render(request,"login.html",context_dict)

def logout_view(request):
    logout(request)
    return redirect('/login/')

def signup(request):
    return HttpResponse(" Hi Sign Up Here ")



def forgot(request):
    return HttpResponse("Your Password has been emailed ! :) ")