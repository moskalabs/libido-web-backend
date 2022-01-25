from django.db import models
from django.utils import timezone

from core.models import TimeStampModel


class User(TimeStampModel):
    email = models.EmailField(max_length=250, unique=True)
    password = models.CharField(max_length=300)
    name = models.CharField(max_length=30, null=True)
    nickname = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=30)
    profile_image_url = models.URLField(max_length=2000, null=True)
    is_receive_email = models.BooleanField(default=False)
    description = models.TextField(null=True)
    day_of_birth = models.CharField(max_length=30, null=True)
    nation = models.CharField(max_length=30)
    login_method = models.CharField(max_length=30, null=True)
    platform_id = models.CharField(max_length=100, null=True)
    reset_token_number = models.CharField(max_length=30, null=True)
    user_histories = models.ManyToManyField(
        "rooms.Room", through="rooms.UserRoomHistory", related_name="users_histories"
    )

    @property
    def followers(self):
        followers = Follow.objects.filter(users=self).order_by("-id")
        return followers

    class Meta:
        db_table = "users"


class Follow(models.Model):
    users = models.ForeignKey(
        "user", on_delete=models.CASCADE, related_name="follow_by_users"
    )
    followed = models.ForeignKey(
        "user", on_delete=models.CASCADE, related_name="foolow_by_followed"
    )

    created_at = models.DateTimeField(
        db_index=True,
        default=timezone.localtime,
        help_text="팔로우 추가한 시간",
    )

    @classmethod
    def follow(cls, user_id, followed_user_id):
        # exception 및 예외처리 구현 필요
        follow = cls.objects.create(
            users=user_id,
            followed=followed_user_id,
        )
        return follow

    @classmethod
    def unfollow(cls, user_id, followed_user_id):
        # exception 및 예외처리 구현 필요
        follow = cls.objects.get(
            users=user_id,
            followed=followed_user_id,
        )
        follow.delete()
        return True

    class Meta:
        db_table = "follows"
