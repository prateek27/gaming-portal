from django.shortcuts import render
from django.http import HttpResponse
from login.models import UserProfile
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
		
		context_dict = {'username':uName,'fullName':uFullName,'photoUrl':uPhoto,
		'website':uWebsite,'email':uEmail}
		return render(request,"user/user_profile.html",context_dict)
	else:
		return HttpResponse("You are Not Logged In !")

def all_users_view(request):
	user_list = User.objects.all()
	context_dict = { 'users':user_list}

	return render(request,"user/all_users.html",context_dict)