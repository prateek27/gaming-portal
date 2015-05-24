from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from games.models import GameSubmission,GameDetail
# Create your views here.
def home_view(request):
	#if request.user.is_authenticated():
	#	return render('home/index.html')

	return render(request,'home/index.html')
def about_view(request):
	return HttpResponse("This is HomePage")
def users_view(request):
	return HttpResponse("This is HomePage")
def news_feed(request):
	recent_feed = GameSubmission.objects.all().order_by('-timestamp')
	context_dict = { 'feed':recent_feed }
	return render(request,"home/feed.html",context_dict)