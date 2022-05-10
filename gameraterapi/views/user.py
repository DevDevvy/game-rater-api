from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gameraterapi.models.gamer import Gamer
from django.contrib.auth.models import User

class UserView(ViewSet):
    """Level up users view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 


    
    def list(self, request):
        """Handle GET requests to get all users

        Returns:
            Response -- JSON serialized list of users
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        
        serializer = UserSerializer(gamer)
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users
    """
    class Meta:
        model = Gamer
        fields = ('id', 'user_id')
