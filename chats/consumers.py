import json

from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer

from rooms.models import Room
from chats.models import Message, ChatRoom


class KeepUserConsumerMixin:
    channel_session = True

    @staticmethod
    def _save_user(func):
        def wrapper(message, **kwargs):
            if message.user is not None and message.user.is_authenticated():
                message.channel_session["user_id"] = message.user.id
            return func(message, **kwargs)

        return wrapper

    def __getattribute__(self, name):
        method = super().__getattribute__(name)
        if name == "connect":
            return self._save_user(method)
        return method

    @property
    def user(self):
        if not hasattr(self, "_user"):
            user_id = self.message.channel_session["user_id"]
            self._user = get_user_model().objects.get(id=user_id)
        return self._user


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # create room
        await self.create_room(room_id=self.room_name)

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]
        room = data["room"]

        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message, "username": username},
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({"message": message, "username": username})
        )

    @sync_to_async
    def create_room(self, room_id):
        Room.objects.get_or_create(id=room_id, is_public=True)

    @sync_to_async
    def save_message(self, username, room, message):
        Message.objects.create(username=username, room=room, content=message)


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # create room
        await self.create_room(room_id=self.room_name)

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]
        room = data["room"]

        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message, "username": username},
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({"message": message, "username": username})
        )

    @sync_to_async
    def create_room(self, room_id):
        Room.objects.get_or_create(id=room_id, is_public=False)

    @sync_to_async
    def save_message(self, username, room, message):
        Message.objects.create(username=username, room=room, content=message)
