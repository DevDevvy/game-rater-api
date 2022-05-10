from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gameraterapi.models import Category
from gameraterapi.models.game_category import Game_Category
from gameraterapi.models.gamer import Gamer

class GameCategoryView(ViewSet):

    def retrieve(self, request, pk):
        
        try:
            gameCategory = Game_Category.objects.get(pk=pk)
            serializer = GameCategorySerializer(gameCategory)
            return Response(serializer.data)
        except Game_Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
    

    def list(self, request):
        """Handle GET requests to get all categories

        Returns:
            Response -- JSON serialized list of categories
        """
        game_categories = Game_Category.objects.all()
        # check if string is a query ie /game_categories?game_id=1
        category = request.query_params.get('category', None)
        if category is not None:
            game_categories = game_categories.filter(game_id=category)
        
        serializer = GameCategorySerializer(game_categories, many=True)
        return Response(serializer.data)


class GameCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = Game_Category
        fields = ('id', 'game_id', 'category_id')

# validates and saves new game
class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Game_Category
        fields = ['id', 'game_id', 'category_id']