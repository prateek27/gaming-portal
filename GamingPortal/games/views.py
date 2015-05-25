from django.shortcuts import render
from django.http import HttpResponse
from games.models import GameDetail,GameSubmission
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def games_view(request):
	game_list = GameDetail.objects.all()
	context_dict={"game_list":game_list}
	return render(request,"games/game_new.html",context_dict)

def launch_game_view(request,game_name):
	#Check if the game exists	
	print(game_name)
	return render(request,"games/"+game_name+".html",{})
	"""
	try:  
		g = GameDetail.objects.get(GameDetail.game_slug_field=game_name)
		return render(request,"games/"+game_name+".html",{})
	except:
		return HttpResponse(game_name+"Game Doesn't Exist")
	"""

@csrf_exempt
def save_score(request):
	user = request.user
	game_id=request.POST.get('game_id')
	game_score = request.POST.get('score')

	print(game_id)
	print(game_score)
	user = request.user
	print(user.id)
	print(user.username)
	
	game = GameDetail.objects.get(id=game_id)
	print(game.game_name)
	submission = GameSubmission.objects.create(game=game,user=user,score=game_score)
	
	return HttpResponse("Ok")