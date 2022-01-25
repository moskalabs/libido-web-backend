import logging
import os
import jwt
import json
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import exceptions
from rest_framework import authentication

from django.contrib.auth import get_user_model
from users.models import User


request_logger = logging.getLogger("default")


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            access_token = request.headers.get("Authorization", None)
            data = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
            )
            user = User.objects.get(id=data["id"])
            return (user, None)

        except jwt.exceptions.DecodeError:
            return None

        except Exception as e:
            return None
