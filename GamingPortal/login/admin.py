from django.contrib import admin
from login.models import *
from django.contrib.auth.models import User 

# Register your models here.
class UserInline(Admin.StackedInline):
	model = UserProfile
	can_delete = False

class UserAdmin(UserAdmin):
	inlines =(UserInline,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)