"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os


from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chats.routing import websocket_urlpatterns


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": application,
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
