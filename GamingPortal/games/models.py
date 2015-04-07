from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class GameDetail(models.Model):
	game_name = models.CharField(max_length=128,blank=False)
	game_image = models.ImageField(upload_to="games_image/",blank=True)
	game_slug_field = models.CharField(max_length=128)
	game_highscore =models.IntegerField(default=0)
	game_highscorer = models.ForeignKey(User)

	def __str__(self):
		return self.game_name

class GameSubmission(models.Model):
	game = models.ForeignKey(GameDetail)
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now_add = True)
	score = models.IntegerField(default=0)

	def __str__(self):
		return self.game.game_name 