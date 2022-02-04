from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rooms.models import Room, RoomCategory, RoomContent


class RoomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCategory
        fields = "__all__"


class RoomContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomContent
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    category = RoomCategorySerializer(allow_null=True, read_only=True)
    # contents = RoomContentSerializer(many=True, allow_null=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
        excludes = ["room_categories"]
