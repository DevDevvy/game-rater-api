"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from gamerraterreports.views.helpers import dict_fetch_all


class Top3ReviewersList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get top 3 game reviewers
            db_cursor.execute("""
            SELECT u.id, u.first_name ||' '|| u.last_name AS name, u.username, COUNT(r.gamer_id) count
            FROM gameraterapi_gamer g
            LEFT JOIN gameraterapi_review r
                ON g.id = r.gamer_id
            JOIN auth_user u
                ON g.user_id = u.id
            GROUP BY g.id
            ORDER BY count DESC
            LIMIT 3
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
            
            top_reviewers_list = []
            
            for row in dataset:
                category = {
                    "id": row['id'],
                    "name": row['name'],
                    "count": row['count'],
                }
                top_reviewers_list.append(category)


                # See if the gamer has been added to the events_by_user list already
                
        # The template string must match the file name of the html template
        template = 'gamers/top_reviewers.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "topreviewers_list": top_reviewers_list
        }

        return render(request, template, context)