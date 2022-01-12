from django.db import models

from core.models    import TimeStampModel


class Room(TimeStampModel):
    title            = models.CharField(max_length=100)
    description      = models.TextField(null=True)
    is_public        = models.BooleanField()
    password         = models.CharField(max_length=50)
    users            = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='rooms')
    room_categories  = models.ForeignKey('RoomCategory', on_delete=models.CASCADE, related_name='rooms')
    rooms_contents   = models.ManyToManyField('contents.Content', through="RoomContent", related_name="rooms")
    running_time     = models.CharField(max_length=20, null=True)
    status           = models.BooleanField(default=False)
    maximum_limit    = models.IntegerField()
    
    class Meta:
        db_table = 'rooms'


class RoomCategory(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'room_categories'


class UserRoomHistory(TimeStampModel):
    rooms = models.ForeignKey('Room', on_delete=models.CASCADE)
    users = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_room_histories'


class RoomContent(TimeStampModel):
    rooms    = models.ForeignKey('Room', on_delete=models.CASCADE)
    contents = models.ForeignKey('contents.Content', on_delete=models.CASCADE)

    class Meta:
        db_table = 'room_contents'