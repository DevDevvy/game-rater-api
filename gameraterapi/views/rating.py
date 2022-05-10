from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gameraterapi.models.gamer import Gamer
from gameraterapi.models.game import Game
from gameraterapi.models.rating import Rating

class RatingView(ViewSet):

    def retrieve(self, request, pk):
        
        try:
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating)
            return Response(serializer.data)
        except Rating.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    # create a new rating
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized rating instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['game_id'])
        serializer = CreateRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer, game=game)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def list(self, request):
        """Handle GET requests to get all categories

        Returns:
            Response -- JSON serialized list of categories
        """
        ratings = Rating.objects.all()
        game = request.query_params.get('game', None)
        # check if string is a query ie /?game=1
        if game is not None:
            ratings = ratings.filter(game_id=game)
        
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)


class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = Rating
        fields = ('id', 'rating', 'game_id', 'gamer_id')

# validates and saves new rating
class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [ 'rating', 'game_id']