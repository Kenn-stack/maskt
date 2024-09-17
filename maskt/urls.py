from django.urls import path, include
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('room/create/', views.create_room, name='create_room'),
    path('room/<id>/', views.chat_room, name='chat_room'),
]
