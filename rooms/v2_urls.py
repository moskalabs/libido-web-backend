from django.conf.urls import include, url
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from rooms.views import RoomViewSet


room_router = DefaultRouter(trailing_slash=False)
room_router.register(r"rooms", RoomViewSet, basename="follow")

urlpatterns = [
    url(r"^", include(room_router.urls)),
]
