import uuid
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gameraterapi.models.game import Game
from gameraterapi.models.gamer import Gamer
from gameraterapi.models.photo import Photo
from django.core.files.base import ContentFile
import base64
class PhotoView(ViewSet):
    """Level up photo types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single photo type

        Returns:
            Response -- JSON serialized photo type
        """
        try:
            photo = Photo.objects.get(pk=pk)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        except Photo.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    # create a new photo
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized photo instance
        """
        # Create a new instance of the game picture model you defined
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['game_id'])
        format, imgstr = request.data["game_image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile   (base64.b64decode(imgstr), name=f'{request.data["game_id"]}-{uuid.uuid4()}.{ext}')
        
        new_photo = Photo.objects.create(
            game=game,
            gamer=gamer,
            game_photo=data
        )
        
        
        serializer = CreatePhotoSerializer(new_photo)
        new_photo.save()
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def list(self, request):
        """Handle GET requests to get all photos

        Returns:
            Response -- JSON serialized list of photos
        """
        photos = Photo.objects.all()
        # check if string is a query ie /photos?type=1
        image_game = request.query_params.get('game', None)
        if image_game is not None:
            images = images.filter(game_id=image_game)

        
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)

   
    
    def destroy(self, request, pk):
        photo = Photo.objects.get(pk=pk)
        photo.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class PhotoSerializer(serializers.ModelSerializer):
    """JSON serializer for photo 
    """
    class Meta:
        model = Photo
        fields = ('id', 'game_id', 'gamer_id', 'game_photo')

# validates and saves new photo
class CreatePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = [ 'game_photo' ]
        

