from django.urls import path
from .views import RoomListView, FriendRoomView

urlpatterns = [
    path("", RoomListView.as_view()),
    path("friends", FriendRoomView.as_view()),
]

