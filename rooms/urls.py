from django.urls import path
from .views import RoomListView, FriendRoomView, SearchRoomView

urlpatterns = [
    path('', RoomListView.as_view()),
    path('/friends', FriendRoomView.as_view()),
    path('/search',SearchRoomView.as_view()),
]
