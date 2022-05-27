"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from gamerraterreports.views.helpers import dict_fetch_all


class BottomRatedGamesList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get top 5 games
            db_cursor.execute("""
            SELECT g.id, AVG(r.rating) avg_rating, g.title 
            FROM gameraterapi_game g
            JOIN gameraterapi_rating r
                ON g.id = r.game_id
            GROUP BY g.id
            ORDER BY avg_rating ASC
            LIMIT 5
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
            
            games = []
            
            for row in dataset:
                game = {
                    "id": row['id'],
                    "avg_rating": row['avg_rating'],
                    "game": row['title']
                }
                games.append(game)


                # See if the gamer has been added to the events_by_user list already
                
        # The template string must match the file name of the html template
        template = 'games/bottom_5_games.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "bottom5games_list": games
        }

        return render(request, template, context)