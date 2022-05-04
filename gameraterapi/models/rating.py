
from django.db import models

class Rating(models.Model):
    rating = models.IntegerField()
    gamer = models.ForeignKey("gamer", on_delete=models.CASCADE)
    game = models.ForeignKey("game", on_delete=models.CASCADE)