from django.db import models

class Photo(models.Model):
    game = models.ForeignKey("game", on_delete=models.DO_NOTHING, related_name="pictures")
    gamer = models.ForeignKey("gamer", on_delete=models.CASCADE)
    game_photo = models.ImageField(
        upload_to='actionimages', height_field=None,
        width_field=None, max_length=None, null=True)