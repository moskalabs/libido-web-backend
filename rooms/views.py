import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from django.contrib.admin.utils import flatten

from rooms.models import Room, RoomCategory
from users.models import User, Follow
from contents.models import Content
from chats.models import Message
from core.views import login_required


class RoomListView(View):
    @login_required
    def get(self, request):
        category = request.GET.get("category")
        user = request.user if request.user != None else None
        OFFSET = int(request.GET.get("offset", 0))
        LIMIT = int(request.GET.get("display", 8))

        q = Q()
        ordering_priority = []

        if category == "customize":
            hitoryies = user.user_histories.all().prefetch_related(
                "rooms_contents", "rooms_contents__content_tags"
            )

            if hitoryies:
                sort = "-view_count"
                ordering_priority.append(sort)

                tag_list = set(
                    [
                        tags.id
                        for history in hitoryies
                        for content in history.rooms_contents.all()
                        for tags in content.content_tags.all()
                    ]
                )
                q.add(Q(content_tags__id__in=tag_list), q.AND)

            else:
                sort = ["?", "-view_count"]
                ordering_priority.extend(sort)

        if category == "popular":
            sort = "-created_at"
            ordering_priority.append(sort)

        contents = (
            Content.objects.filter(q)
            .select_related("content_categories")
            .prefetch_related("rooms", "rooms__rooms_contents")
            .order_by(*ordering_priority)
            .distinct()
        )
        rooms = [
            flatten(content.rooms.all())
            for content in contents
            if content.rooms.all().exists()
        ]

        result = [
            {
                "id": room.id,
                "category": room.rooms_contents.first().content_categories.name,
                "is_public": room.is_public,
                "password": room.password,
                "link_url": room.rooms_contents.first().content_link_url,
                "title": room.title,
                "title": room.description,
                "nickname": room.users.nickname,
                "image_url": room.rooms_contents.first().thumbnails_url,
                "published_at": room.created_at,
            }
            for room in flatten(rooms)[OFFSET : OFFSET + LIMIT]
        ]

        return JsonResponse({"message": result}, status=200)


class FriendRoomView(View):
    @login_required
    def get(self, request):
        user = request.user
        OFFSET = int(request.GET.get("offset", 0))
        LIMIT = int(request.GET.get("display", 8))

        follows = (
            Follow.objects.filter(users_id=user.id)
            .select_related("followed")
            .prefetch_related("followed__rooms", "followed__rooms__rooms_contents")
        )
        rooms = [room for follow in follows for room in follow.followed.rooms.all()]

        result = [
            {
                "id": room.id,
                "category": room.room_categories.name,
                "is_public": room.is_public,
                "password": room.password,
                "link_url": room.rooms_contents.first().content_link_url,
                "title": room.title,
                "title": room.description,
                "nickname": room.users.nickname,
                "image_url": room.rooms_contents.first().thumbnails_url,
                "published_at": room.created_at,
            }
            for room in rooms[OFFSET : OFFSET + LIMIT]
        ]
        return JsonResponse({"message": result}, status=200)


def index(request):
    # no need auth ?
    return render(request, "rooms/index.html")


def room(request, room_name):
    # check oauth2 ?
    username = request.GET.get("username", "Anonymous")
    messages = Message.objects.filter(room=room_name)[0:25]

    return render(
        request,
        "rooms/room.html",
        {"room_name": room_name, "username": username, "messages": messages},
    )
