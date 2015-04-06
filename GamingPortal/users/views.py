from django.shortcuts import render

# Create your views here.
def user_profile_view(request):
	return render(request,"user/user_profile.html")