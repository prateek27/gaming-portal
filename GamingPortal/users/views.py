from django.shortcuts import render
from django.http import HttpResponse
from login.models import UserProfile
from games.models import GameDetail,GameSubmission
from django.contrib.auth.models import User
# Create your views here.
def user_profile_view(request):
	if request.user.is_authenticated():
		current_user = request.user
		
		uName = current_user.username
		uFullName = current_user.first_name + " " + current_user.last_name
		uEmail = current_user.email
		
		
		user_profile = UserProfile.objects.get(user=current_user)
		uPhoto = user_profile.profile_image.path
		uWebsite = user_profile.profile_url

		substr = "/media/"
		position = uPhoto.find(substr)
		uPhoto = uPhoto[position:]

		#Query for Game Highscores and highscorers 
		game_list = GameDetail.objects.all()
		
		context_dict = {'username':uName,'fullName':uFullName,'photoUrl':uPhoto,
		'website':uWebsite,'email':uEmail,'game_list':game_list}
		return render(request,"user/user_profile.html",context_dict)
	else:
		return HttpResponse("You are Not Logged In !")


def all_users_view(request):
	user_list = User.objects.all()
	

	y=User.objects.get(username="prateek")
	pic_dict={}
	new_user_list = []
	for x in user_list:
		user_full = x
		
		#print(user_full.username+user_full.photo)
		user_profile = UserProfile.objects.filter(user=x)
		if user_profile.count()==0:
			user_full.photo = ""
		else:
			user_full.photo="/media/"+ str(user_profile[0].profile_image)

		new_user_list.append(user_full)
	
	context_dict = { 'users':new_user_list ,'pics':pic_dict}
	print(pic_dict)
	return render(request,"user/all_users.html",context_dict)