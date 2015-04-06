from django.shortcuts import render

# Create your views here.

def games_view(request):
	return render(request,"games/games.html")