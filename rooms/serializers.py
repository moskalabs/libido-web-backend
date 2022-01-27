from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rooms.models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
