from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	profile_url = models.URLField(blank=True)
	profile_image = models.ImageField(upload_to="profile_image/",default="profile_image/default1.jpg")

	def __str__(self):
		return self.user.username