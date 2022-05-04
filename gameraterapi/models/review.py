
from django.db import models

class Review(models.Model):
    review = models.CharField(max_length=500)
    gamer = models.ForeignKey("gamer", on_delete=models.CASCADE)
    game = models.ForeignKey("game", on_delete=models.CASCADE)