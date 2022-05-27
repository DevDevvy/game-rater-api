"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from gamerraterreports.views.helpers import dict_fetch_all


class CategoryGamesCountList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get how many games in each category
            db_cursor.execute("""
            SELECT c.*, COUNT(gc.id) AS game_count
            FROM gameraterapi_category c
            JOIN gameraterapi_game_category gc
                ON c.id = gc.category_id
            GROUP BY c.category
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
            
            category_games_count = []
            
            for row in dataset:
                category = {
                    "id": row['id'],
                    "category": row['category'],
                    "game_count": row['game_count'],
                }
                category_games_count.append(category)


                # See if the gamer has been added to the events_by_user list already
                
        # The template string must match the file name of the html template
        template = 'games/games_by_category.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "gamescountbycategory_list": category_games_count
        }

        return render(request, template, context)