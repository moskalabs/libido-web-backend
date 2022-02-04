from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from contents.models import Content


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"
