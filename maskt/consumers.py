import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.template.loader import get_template

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import DenyConnection, StopConsumer
from channels_presence.decorators import touch_presence

from .models import Message
from channels_presence.models import Presence, Room

from haikunator import Haikunator


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        try:
            haikunator = Haikunator()
            self.sender = haikunator.haikunate(token_length=0)
            self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
            print(self.room_id)
            self.room = Room.objects.get(room_id=self.room_id)
        except Room.DoesNotExist:
           raise StopConsumer()
        
        self.room_group_name = self.room.channel_name

        # Join room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name, self.channel_name
        # )
        Room.objects.add(self.room_group_name, self.channel_name)
        online_count = self.room.get_anonymous_count()
        html = get_template('partials.html').render(context={'online_count': online_count})

        self.accept()
        print(online_count)
        self.send(text_data=html)
        


    def disconnect(self, close_code):
        # Leave room group
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name, self.channel_name
        # )

        Room.objects.remove(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    # @touch_presence
    def receive(self, text_data):
        if text_data == '"heartbeat"':
            Presence.objects.touch(self.channel_name)
        else:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            # message = (self.sender + ' >>> ' + message)
            

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat.message", "message": message, "sender": self.sender}
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        Message.objects.create(comment=message, sender=sender, room=self.room)
        my_message = sender == self.sender

        context = {'message': message, 'sender': sender, 'my_message': my_message}
        html = get_template('partials.html').render(context=context)

        print('about to send')
        # Send message to WebSocket
        self.send(text_data=html)

    
    def forward_message(self, event):
        online_count = event["online"]
        html = get_template('partials.html').render(context={'online_count': online_count})


        # Send message to WebSocket
        self.send(text_data=html)

