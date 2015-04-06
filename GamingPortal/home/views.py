from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.
def home_view(request):
	if request.user.is_authenticated():
		return render('home/index.html')

	return render(request,'home/index.html')
def about_view(request):
	return HttpResponse("This is HomePage")
def users_view(request):
	return HttpResponse("This is HomePage")