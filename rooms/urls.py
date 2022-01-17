from django.urls import path
from .views import RoomListView, FriendRoomView, index, room

urlpatterns = [
    path("", RoomListView.as_view()),
    path("/friends", FriendRoomView.as_view()),
    path("/chat", index, name="index"),
    path("/rooms/<str:room_name>/", room, name="room"),
]
