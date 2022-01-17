from django.urls import path
from chats import consumers

websocket_urlpatterns = [
    path("ws/group_chat/<str:room_name>/", consumers.GroupChatConsumer.as_asgi()),
    path("ws/private_chat/<str:room_name>/", consumers.PrivateChatConsumer.as_asgi()),
    # path("ws/group_chat/<str:room_name>/", consumers.GroupChatConsumer.as_asgi()),
    # path("ws/private_chat/<str:room_name>/", consumers.PrivateChatConsumer.as_asgi()),
]
