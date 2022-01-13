import secrets
from django.db import models

from core.models import TimeStampModel


def _generate_room_random_id(_len=35):
    return secrets.token_urlsafe(_len)


class Room(TimeStampModel):
    # 방의 아이디는 random hash로 처리한다 (보안이슈)
    id = models.CharField(
        db_index=True,
        max_length=55,
        default=_generate_room_random_id,
        primary_key=True,
    )

    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    is_public = models.BooleanField()
    password = models.CharField(max_length=50)
    users = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="rooms"
    )
    room_categories = models.ForeignKey(
        "RoomCategory", on_delete=models.CASCADE, related_name="rooms"
    )
    rooms_contents = models.ManyToManyField(
        "contents.Content", through="RoomContent", related_name="rooms"
    )

    class Meta:
        db_table = "rooms"


class RoomCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "room_categories"


class UserRoomHistory(TimeStampModel):
    rooms = models.ForeignKey("Room", on_delete=models.CASCADE)
    users = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        db_table = "user_room_histories"


class RoomContent(TimeStampModel):
    rooms = models.ForeignKey("Room", on_delete=models.CASCADE)
    contents = models.ForeignKey("contents.Content", on_delete=models.CASCADE)

    class Meta:
        db_table = "room_contents"
