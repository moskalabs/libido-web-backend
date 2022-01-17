import datetime
from datetime import timedelta
from enum import IntEnum
from io import BytesIO
import json
import os
import random
import secrets
import sys
import time
import uuid

import bcrypt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher, make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.gis.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Count, Sum
from django.db.models import Q
from django.db.utils import IntegrityError
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _


def _generate_room_random_id(_len=30):
    return secrets.token_urlsafe(_len)


class ThingChatRoomType(models.IntegerChoices):
    GROUP_CHAT = 0, "Group Chat"
    DM = 1, "Direct Message"


class ChatRoom(models.Model):
    #  해당모델 사용안할것임
    id = models.CharField(
        db_index=True,
        max_length=55,
        default=_generate_room_random_id,
        primary_key=True,
    )

    user_type = models.IntegerField(
        choices=ThingChatRoomType.choices,
        default=ThingChatRoomType.GROUP_CHAT,
        verbose_name="채팅방 유형",
        help_text="채팅방 유형",
    )

    created_at = models.DateTimeField(
        verbose_name="작성한 시간",
        db_index=True,
        default=timezone.now,
        help_text="메세지 작성한 시간",
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = "채팅방"
        verbose_name_plural = "채팅방 모음"
        db_table = "chat_room"
        managed = True


class Message(models.Model):
    username = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(
        verbose_name="작성한 시간",
        db_index=True,
        default=timezone.now,
        help_text="메세지 작성한 시간",
    )

    def __str__(self):
        return f"{self.username}"

    class Meta:
        ordering = ("created_at",)
        verbose_name = "채팅 메세지"
        verbose_name_plural = "채팅 메세지 모음"
        db_table = "message"
        managed = True
