"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from gamerraterreports.views.helpers import dict_fetch_all


class GamesWithNoPicturesList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to find how many games don't have pictures
            db_cursor.execute("""
            SELECT g.*
            FROM gameraterapi_game g
            LEFT JOIN gameraterapi_photo p 
                ON  g.id = p.game_id
            WHERE p.id ISNULL
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
            
            games = []
            
            for row in dataset:
                game = {
                    "id": row['id'],
                    "title": row['title']
                }
                games.append(game)


                # See if the gamer has been added to the events_by_user list already
                
        # The template string must match the file name of the html template
        template = 'games/games_with_no_pictures_count.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "nopics_list": games
        }

        return render(request, template, context)