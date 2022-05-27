"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from gamerraterreports.views.helpers import dict_fetch_all


class GamerWithMostAddedGamesList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get which player has the most games added
            db_cursor.execute("""
            SELECT gr.id AS gamer_id, u.first_name ||' '|| u.last_name AS Name, COUNT(g.id) AS count
            FROM gameraterapi_gamer gr
            JOIN gameraterapi_game g
                ON gr.id = g.gamer_id
            JOIN auth_user u
                ON gr.user_id = u.id
            GROUP BY Name
            ORDER BY count DESC
            LIMIT 1
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
            
        # The template string must match the file name of the html template
        template = 'gamers/most_games_added_by_player.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "gamesaddedbyplayer_list": dataset
        }

        return render(request, template, context)