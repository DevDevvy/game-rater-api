
from django.db import models

from gameraterapi.models.rating import Rating

class Game(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    designer = models.CharField(max_length=40)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    est_time_to_play = models.IntegerField()
    age_rec = models.IntegerField()
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    category = models.ManyToManyField("Category", related_name="categories")
    
    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = Rating.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        if ratings:
            for rating in ratings:
                total_rating += rating.rating
            average = total_rating/len(ratings)
        else:
            average = 0
            return average
        # Calculate the averge and return it.
        # If you don't know how to calculate averge, Google it.