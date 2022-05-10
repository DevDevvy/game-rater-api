from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gameraterapi.models.gamer import Gamer

class GamerView(ViewSet):
    """Level up game types view"""



    
    def list(self, request):
        """Handle GET requests to get all game

        Returns:
            Response -- JSON serialized list of game types
        """
        gamers = Gamer.objects.get(user=request.auth.user)
        serializer = GamerSerializer(gamers)
        return Response(serializer.data)


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for game
    """
    class Meta:
        model = Gamer
        fields = ('id', 'user_id')
        depth = 1
        
