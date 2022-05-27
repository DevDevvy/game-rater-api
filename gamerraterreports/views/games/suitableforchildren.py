"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from gamerraterreports.views.helpers import dict_fetch_all


class GamesForChildrenList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get games suitable for children
            db_cursor.execute("""
            SELECT g.id, g.title, g.age_rec
            FROM gameraterapi_game g
            WHERE g.age_rec < 8
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
            
            games = []
            
            for row in dataset:
                game = {
                    "id": row['id'],
                    "title": row['title'],
                    "age_rec": row['age_rec']
                }
                games.append(game)


                # See if the gamer has been added to the events_by_user list already
                
        # The template string must match the file name of the html template
        template = 'games/suitable_for_children_under_8.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "childrensgames_list": games
        }

        return render(request, template, context)