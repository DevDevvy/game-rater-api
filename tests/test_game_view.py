from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from gameraterapi.models.game import Game

from gameraterapi.models.gamer import Gamer
from gameraterapi.models.rating import Rating
from gameraterapi.views.game import CreateGameSerializer, GameSerializer


class GameTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_categories', 'game', 'categories', 'rating']

    def setUp(self):
        # Grab the first Gamer object from the database and add their token to the headers
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_game(self):
        """Create game test"""
        url = "/games"

        # Define the Game properties
        # The keys should match what the create method is expecting
        # Make sure this matches the code you have
        game = {
            "title": "Clue",
            "description": "Milton Bradley's school night fun",
            "designer": "ToysRYous",
            "year_released": 600,
            "number_of_players": 4,
            "est_time_to_play": 60,
            "age_rec": 9,
            "category_id": 2
        }

        response = self.client.post(url, game, format='json')

        # The _expected_ output should come first when using an assertion with 2 arguments
        # The _actual_ output will be the second argument
        # We _expect_ the status to be status.HTTP_201_CREATED and it _actually_ was response.status_code
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # Get the last game added to the database, it should be the one just created
        new_game = Game.objects.last()

        # Since the create method should return the serialized version of the newly created game,
        # Use the serializer you're using in the create method to serialize the "new_game"
        # Depending on your code this might be different
        expected = CreateGameSerializer(new_game)

        # Now we can test that the expected ouput matches what was actually returned
        self.assertEqual(expected.data, response.data)

# test to get single game
    def test_get_game(self):
        """Get Game Test
        """
        # Grab a game object from the database
        game = Game.objects.first()

        url = f'/games/{game.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Like before, run the game through the serializer that's being used in view
        expected = GameSerializer(game)

        # Assert that the response matches the expected return data
        self.assertEqual(expected.data, response.data)
# test to list
    def test_list_games(self):
        """Test list games"""
        url = '/games'

        response = self.client.get(url)

        # Get all the games in the database and serialize them to get the expected output
        all_games = Game.objects.all()
        expected = GameSerializer(all_games, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertEqual(expected.data, response.data)

    def test_change_game(self):
        """test update game"""
        # Grab the first game in the database
        game = Game.objects.first()

        url = f'/games/{game.id}'

        updated_game = {
            "title": f'{game.title} updated',
            "description": game.description,
            "designer": game.designer,
            "number_of_players": game.number_of_players,
            "year_released": game.year_released,
            "est_time_to_play": game.est_time_to_play,
            "age_rec": game.age_rec,
        }

        response = self.client.put(url, updated_game, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Refresh the game object to reflect any changes in the database
        game.refresh_from_db()

        # assert that the updated value matches
        self.assertEqual(updated_game['title'], game.title)
        
    # test to rate game (rating and game_id)
    def test_rate_game(self):
        """Create game rating"""
        url = "/ratings?game=1"
        
        rating = {
            "rating": 3,
        }
        
        response = self.client.post(url, rating, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
    def test_change_rating(self):
        """test update rating"""
    
        rating = Rating.objects.first()

        url = f'/ratings/{rating.id}'

        updated_rating = {
            "rating": 2,
        }

        response = self.client.put(url, updated_rating, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Refresh the game object to reflect any changes in the database
        rating.refresh_from_db()

        # assert that the updated value matches
        self.assertEqual(updated_rating['rating'], rating.rating)
        
    # test to delete game
    def test_delete_game(self):
        """Delete Game Test
        """
        # Grab a game object from the database
        game = Game.objects.first()

        url = f'/games/{game.id}'

        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Like before, run the game through the serializer that's being used in view
        response = self.client.get(url)
        # Assert that the response matches the expected return data
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        
    def test_review_game(self):
        """Create game review"""
        url = "/reviews"
        
        review = {
            "review": "sweet mapping",
            "game": 2
        }
        
        response = self.client.post(url, review, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
