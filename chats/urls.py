from django.conf.urls import include, url
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from chats.views import ChatRoomsViewSet


default_router = DefaultRouter(trailing_slash=False)
default_router.register(r"chat_rooms", ChatRoomsViewSet, basename="rooms")

urlpatterns = [
    url(r"^", include(default_router.urls)),
]
