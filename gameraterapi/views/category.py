from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gameraterapi.models import Category
from gameraterapi.models.gamer import Gamer

class CategoryView(ViewSet):

    def retrieve(self, request, pk):
        
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    # create a new category
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized category instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def list(self, request):
        """Handle GET requests to get all categories

        Returns:
            Response -- JSON serialized list of categories
        """
        categories = Category.objects.all()
        # check if string is a query ie /categories?type=1
        
        
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = Category
        fields = ('id', 'category')

# validates and saves new game
class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category']