from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from users.models import User, Follow


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class FollowSerializer(serializers.ModelSerializer):
    users_name = serializers.ReadOnlyField(allow_null=True)
    followed_name = serializers.ReadOnlyField(allow_null=True)

    users_nickname = serializers.ReadOnlyField(allow_null=True)
    followed_nickname = serializers.ReadOnlyField(allow_null=True)

    class Meta:
        model = Follow
        fields = [
            "id",
            "users",
            "followed",
            "users_name",
            "followed_name",
            "users_nickname",
            "followed_nickname",
            "created_at",
        ]
