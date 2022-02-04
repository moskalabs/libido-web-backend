from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from contents.models import Content, ContentCategory, ContentTag, Tag


class ContentTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentTag
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ContentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentCategory
        fields = "__all__"


class ContentSerializer(serializers.ModelSerializer):
    category = ContentCategorySerializer(read_only=True, allow_null=True)

    tags = TagSerializer(read_only=True, many=True, allow_null=True)

    class Meta:
        model = Content
        fields = "__all__"
        excludes = ["content_tags", "content_categories"]
