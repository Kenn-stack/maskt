from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels_presence.signals import presence_changed
from django.dispatch import receiver

import json


channel_layer = get_channel_layer()

@receiver(presence_changed)
def broadcast_presence(room, **kwargs):
    """
    Broadcasts the number of active connected channels (online) 
    """
    print('Presence changed')
    online = room.get_anonymous_count()
    print(online)

    channel_layer_message = {
        "type": "forward.message",
        "online": online,
    }

    async_to_sync(channel_layer.group_send)(room.channel_name, channel_layer_message)
