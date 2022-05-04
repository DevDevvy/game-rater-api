from django.db import models


class Game_Category(models.Model):
    game = models.ForeignKey("game", on_delete=models.CASCADE)
    category = models.ForeignKey("category", on_delete=models.CASCADE)