
from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    designer = models.CharField(max_length=40)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    est_time_to_play = models.IntegerField()
    age_rec = models.IntegerField()
    gamer = models.ForeignKey("gamer", on_delete=models.CASCADE)