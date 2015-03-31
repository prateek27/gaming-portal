from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from login.models import UserProfile
from login.forms import LoginForm
# Create your views here.

def some_view(request):
	return HttpResponse("Hello World!")

def login(request):
	if request.method =='POST':
		
		return HttpResponse("Post Request")
	else:
		login_form = LoginForm()
		context_dict = {'form':login_form} 
		return render(request,"login.html",context_dict)

def signup(request):
	return HttpResponse(" Hi Sign Up Here ")



def forgot(request):
	return HttpResponse("Your Password has been emailed ! :) ")