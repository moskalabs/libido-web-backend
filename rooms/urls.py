from django.urls import path
from .views import RoomListView

urlpatterns = [
    path('', RoomListView.as_view()),
]