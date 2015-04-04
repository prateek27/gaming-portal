from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from login.models import UserProfile
from login.forms import LoginForm,UserForm,UserProfileForm

from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.core import serializers
# Create your views here.


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponse("You are already Logged In ") 
    
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

def signup_view(request):
    if request.method == "POST":
        user_profile_form = UserProfileForm(request.POST,request.FILES)
        user_form  = UserForm(request.POST)
        
         
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user;
            if 'profile_image' in request.FILES:
                user_profile.profile_image = request.FILES['profile_image']
            
            user_profile.save()

            return HttpResponse("You are now successfully registered ! ")
        else:
            return HttpResponse("Form Not Valid !")
    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()
        context_dict ={"user_form":user_form,"user_profile_form":user_profile_form};
        return render(request,'signup.html',context_dict)




def forgot_password_view(request):
    return HttpResponse("Your Password has been emailed ! :) ")