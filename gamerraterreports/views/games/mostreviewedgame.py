"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from gamerraterreports.views.helpers import dict_fetch_all


class MostReviewedGameList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get game with most ratings
            db_cursor.execute("""
            SELECT g.id, g.title, COUNT(r.rating) AS number_of_ratings
            FROM gameraterapi_game g
            JOIN gameraterapi_rating r
                ON g.id = r.game_id
            GROUP BY g.id
            ORDER BY number_of_ratings DESC
            LIMIT 1
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
    
        # The template string must match the file name of the html template
        template = 'games/most_reviewed_game.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "mostreviewed_list": dataset
        }

        return render(request, template, context)