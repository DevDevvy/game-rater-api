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
        game = Game.objects.get(pk=request.query_params.get('game', None))
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
        gamer_id = request.query_params.get('gamer', None)
        # check if string is a query ie /?game=1
        if game is not None:
            ratings = ratings.filter(game_id=game)
        if gamer_id is not None:
            ratings = ratings.filter(gamer=gamer_id)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a rating

        Returns:
            Response -- Empty body with 204 status code
        """
        rating = Rating.objects.get(pk=pk)
        serializer = CreateRatingSerializer(rating, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        rating = Rating.objects.get(pk=pk)
        rating.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

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
        fields = [ 'rating']