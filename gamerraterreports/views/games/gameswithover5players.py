"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from gamerraterreports.views.helpers import dict_fetch_all


class Over5PlayersList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get games with over 5 players
            db_cursor.execute("""
            SELECT g.id, g.number_of_players, g.title 
            FROM gameraterapi_game g
            GROUP BY g.title
            HAVING min(g.number_of_players) > 5
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
            
            games = []
            
            for row in dataset:
                game = {
                    "id": row['id'],
                    "title": row['title'],
                    "players": row['number_of_players']
                }
                games.append(game)


                # See if the gamer has been added to the events_by_user list already
                
        # The template string must match the file name of the html template
        template = 'games/games_over_5_players.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "over5players_list": games
        }

        return render(request, template, context)