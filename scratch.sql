SELECT MAX(mycount) AS Count
            FROM (
                SELECT AVG(r.rating) count, g.*, r.* 
                FROM gameraterapi_game g
                JOIN gameraterapi_rating r
                    ON g.id = r.game_id
                GROUP BY g.title
                ORDER BY count DESC
                LIMIT 5
                )

SELECT g.id, AVG(r.rating) avg_rating, g.title 
            FROM gameraterapi_game g
            JOIN gameraterapi_rating r
                ON g.id = r.game_id
            GROUP BY g.id
            ORDER BY avg_rating ASC
            LIMIT 5

            SELECT c.*, COUNT(gc.id)
            FROM gameraterapi_category c
            JOIN gameraterapi_game_category gc
                ON c.id = gc.category_id
            GROUP BY c.category

SELECT g.id, g.number_of_players, g.title 
            FROM gameraterapi_game g
            GROUP BY g.title
            HAVING min(g.number_of_players) > 5

SELECT g.id, g.title, COUNT(r.rating) AS number_of_ratings 
            FROM gameraterapi_game g
            JOIN gameraterapi_rating r
                ON g.id = r.game_id
            GROUP BY g.id
            ORDER BY number_of_ratings DESC
            LIMIT 1

            SELECT gr.id AS gamer_id, u.first_name ||' '|| u.last_name AS Name, COUNT(g.id) AS count
            FROM gameraterapi_gamer gr
            JOIN gameraterapi_game g
                ON gr.id = g.gamer_id
            JOIN auth_user u
                ON gr.user_id = u.id
            GROUP BY Name
            ORDER BY count DESC
            LIMIT 1

            SELECT g.id, g.title, g.age_rec
            FROM gameraterapi_game g
            WHERE g.age_rec < 9


            SELECT g.*
            FROM gameraterapi_game g
            LEFT JOIN gameraterapi_photo p 
                ON  g.id = p.game_id
            WHERE p.id ISNULL


            SELECT u.id, u.first_name ||' '|| u.last_name AS name, u.username, COUNT(r.gamer_id) count
            FROM gameraterapi_gamer g
            LEFT JOIN gameraterapi_review r
                ON g.id = r.gamer_id
            JOIN auth_user u
                ON g.user_id = u.id
            GROUP BY g.id
            ORDER BY count DESC
            LIMIT 5