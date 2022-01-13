from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from rooms.models import Room
from chats.models import Message, ChatRoom
from chats.serializers import MessageSerializer, ChatRoomSerializer, RoomSerializer
from commons.paginations import CommonPagination


# def room(request, room_name):
#     # check oauth2 ?
#     username = request.GET.get("username", "Anonymous")
#     messages = Message.objects.filter(room=room_name)[0:25]

#     return render(
#         request,
#         "offerflow_chats/room.html",
#         {"room_name": room_name, "username": username, "messages": messages},
#     )


class ChatRoomsViewSet(viewsets.ModelViewSet):
    __basic_fields = ("id", "created_at")
    permission_classes = [
        # permissions.AllowRetriveList,
    ]
    # renderer_classes = [LibidoApiJSONRenderer]
    queryset = Room.objects.all().order_by("-id")
    serializer_class = RoomSerializer
    pagination_class = CommonPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filter_fields = __basic_fields
    search_fields = __basic_fields
