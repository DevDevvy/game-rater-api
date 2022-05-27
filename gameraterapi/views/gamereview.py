from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gameraterapi.models import Game
from gameraterapi.models.gamer import Gamer
from gameraterapi.models.review import Review

class GameReviewView(ViewSet):
    """Level up game reviews"""

    def retrieve(self, request, pk):
        """Handle GET requests for single review

        Returns:
            Response -- JSON serialized review
        """
        try:
            review = Review.objects.get(pk=pk)
            serializer = GameReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    # create a new review
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        
        serializer = CreateGameReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # list handles queries
    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        review = Review.objects.all()
        # check if string is a query ie /review?type=1
        game = request.query_params.get('game', None)
        if game is not None:
            review = review.filter(game_id=game)
        
        serializer = GameReviewSerializer(review, many=True)
        return Response(serializer.data)
    
    # added validation 
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)
        serializer = CreateGameReviewSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class GameReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Review
        fields = ('id', 'review', 'game', 'gamer')
        depth = 1
        
# validates and saves new game
class CreateGameReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['review', 'game']