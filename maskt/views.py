from django.shortcuts import redirect, render
from django.urls import reverse
from channels_presence.models import Room

# Create your views here.

def index(request):
    if request.method == "POST":
       id = request.POST.get('id') 
       return redirect(chat_room, id)
    else:
        return render(request, 'index.html')

def create_room(request):
    if request.POST:
        room_name = request.POST.get('room-name')
        print(room_name)
        new_room = Room.objects.create(channel_name=room_name)
        return redirect(reverse('chat_room', args=(new_room.room_id,)))
    else:
        return render(request, 'create_room.html')


def chat_room(request, id):
    return render(request, 'chat_room.html', {'room_id':id})
