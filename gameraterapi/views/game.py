from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gameraterapi.models import Game
from gameraterapi.models.gamer import Gamer
from rest_framework.decorators import action

from gameraterapi.models.rating import Rating
class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    # create a new game
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
    
        game = Game.objects.get(pk=serializer.data["id"])
        game.category.add(request.data["category_id"])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
        # check if string is a query ie /games?type=1
        categories = request.query_params.get('categories', None)
        if categories is not None:
            games = games.filter(games_categories_id=categories)
        
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    # added validation 
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)
        game.title = request.data['title']
        game.designer = request.data['designer']
        game.description = request.data['description']
        game.year_released = request.data['year_released']
        game.number_of_players = request.data['number_of_players']
        game.age_rec = request.data['age_rec']
        game.est_time_to_play = request.data['est_time_to_play']
        game.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    @action(methods=['post'], detail=True)
    def ratings(self, request, pk):
        """Post request for a user to rate game"""
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=pk)
        rating = Rating.objects.create(
            rating=request.data['rating'],
            game=game,
            gamer=gamer
        )
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game 
    """
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'year_released', 'number_of_players', 'est_time_to_play', 'age_rec', 'gamer', 'category', 'average_rating')
        depth = 1
        
# validates and saves new game
class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'description', 'designer', 'year_released', 'number_of_players', 'est_time_to_play', 'age_rec']
        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [ 'rating' ]
