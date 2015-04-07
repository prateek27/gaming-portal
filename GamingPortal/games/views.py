from django.shortcuts import render
from django.http import HttpResponse
from games.models import GameDetail
# Create your views here.

def games_view(request):
	game_list = GameDetail.objects.all()
	context_dict={"game_list":game_list}
	return render(request,"games/game_new.html",context_dict)

def launch_game_view(request,game_name):
	#Check if the game exists	
	try:  
		g = GameDetail.objects.get(game_slug_field=game_name)
		return render(request,"games/"+game_name+".html",{})
	except:
		return HttpResponse(game_name+"Game Doesn't Exist")