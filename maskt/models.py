from django.db import models
import uuid
from .utils import gen_rand

from channels_presence.models import Room



# Create your models here.


# class MyRoomManager(RoomManager):
#     def add(self, room_channel_name, user_channel_name, user=None):
#         room = Room.objects.get(channel_name=room_channel_name)
#         room.add_presence(user_channel_name, user)
#         return room



# class Room(MyRoom):
#     room_id = models.CharField(max_length=50, primary_key=True, default=gen_rand(8))

#     objects = MyRoomManager()


# class Presence(MyPresence):
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)



class Message(models.Model):
    comment = models.TextField(max_length=200)
    sender = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    datetime_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-datetime_stamp"]
