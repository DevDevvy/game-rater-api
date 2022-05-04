
from django.db import models

class Photo(models.Model):
    photo = models.ImageField(upload_to = 'photos/')
    gamer = models.ForeignKey("gamer", on_delete=models.CASCADE)
    game = models.ForeignKey("game", on_delete=models.CASCADE)