import functools
import json
from os       import error
from datetime import datetime

from django.http                import JsonResponse
from django.utils.tree          import Node
from django.views               import View
from django.db.models           import Q
from django.contrib.admin.utils import flatten

from .models           import *
from users.models      import *
from contents.models   import *
from core.utils        import login_required

class RoomListView(View):
    @login_required
    def get(self, request):
        category = request.GET.get('category')
        user     = request.user if request.user != None else None
        OFFSET   = int(request.GET.get('offset', 0))
        LIMIT    = int(request.GET.get('display', 8))

        q = Q()
        ordering_priority = []

        if category == 'customize':
            hitoryies = user.user_histories.all().prefetch_related('rooms_contents', 'rooms_contents__content_tags')

            if hitoryies:
                sort = '-view_count'
                ordering_priority.append(sort)

                tag_list  = set([tags.id for history in hitoryies for content in history.rooms_contents.all() for tags in content.content_tags.all()])
                q.add(Q(content_tags__id__in = tag_list), q.AND)

            else:
                sort = ['?', '-view_count']
                ordering_priority.extend(sort)

        if category == 'popular':
            sort = '-created_at'
            ordering_priority.append(sort)
        
        contents = Content.objects.filter(q).select_related('content_categories').prefetch_related('rooms', 'rooms__rooms_contents').order_by(*ordering_priority).distinct()
        rooms    = [flatten(content.rooms.all()) for content in contents if content.rooms.all().exists()]
        
        result = [
            {   
                'id'            : room.id,
                'category'      : room.rooms_contents.first().content_categories.name,
                'is_public'     : room.is_public,
                'link_url'      : room.rooms_contents.first().content_link_url,
                'title'         : room.title,
                'description'   : room.description,
                'nickname'      : room.users.nickname,
                'image_url'     : room.rooms_contents.first().thumbnails_url,
                'published_at'  : (datetime.now() - room.created_at).seconds // 60,
            } for room in flatten(rooms)[OFFSET:OFFSET+LIMIT]
        ]

        return JsonResponse({'message': result}, status=200)


class FriendRoomView(View):
    @login_required
    def get(self, request):
        user     = request.user
        OFFSET   = int(request.GET.get('offset', 0))
        LIMIT    = int(request.GET.get('display', 8))

        follows = Follow.objects.filter(users_id=user.id).select_related('followed').prefetch_related('followed__rooms', 'followed__rooms__rooms_contents')
        rooms = [room for follow in follows for room in follow.followed.rooms.all()]

        result = [
                {   
                    'id'           : room.id,
                    'category'     : room.room_categories.name,
                    'is_public'    : room.is_public,
                    'link_url'     : room.rooms_contents.first().content_link_url,
                    'title'        : room.title,
                    'description'  : room.description,
                    'nickname'     : room.users.nickname,
                    'image_url'    : room.rooms_contents.first().thumbnails_url,
                    'published_at' : (datetime.now() - room.created_at).seconds // 60,
                } for room in rooms[OFFSET:OFFSET+LIMIT]
            ]    

        return JsonResponse({'message': result}, status=200)

class SearchRoomView(View):
    def get(self, request):
        '''
        1. 요청
        - room name
        - content name
        - nick name
        - text (keyword)
        - Category (유튜브, 넷플릭스)
        - 실시간 시청자 수 (방 만들며 생기는 maximum)
        - 플레이 리스트 갯수 이하
        - 공개 or 비공개
        http://127.0.0.1:8000/rooms/search?searchoption=roomname
        '''
        where     = request.GET.get('where',None)
        keyword   = request.GET.get('keyword',None)
        viewers   = request.GET.get('viewers',None)
        playlists = request.GET.get('playlists',None)
        public    = request.GET.get('public',None)
        OFFSET    = int(request.GET.get('offset',0))
        LIMIT     = int(request.GET.get('display',12))

        q = Q()
        
        FILTERS = {
            'roomname'    : Q('rooms__title'),
            'contentname' : Q('rooms__roomcontent__contents__name'),
            'nickname'    : Q('users__nickname'),
            'viewers'     : Q(''),
            'playlists'   : Q('rooms__created_at'),
            'pulic'       : Q('rooms__is_public'),
        }
        Room.objects.filter(title__icontains=keyword)

        result = [
            {
                'id'           : room.id,
                'category'     : room.rooms_contents.first().content_categories.name,
                'is_public'    : room.is_public,
                'keyword'      : keyword,
                'link_url'     : room.rooms_contents.first().content_link_url,
                'title'        : room.title,
                'description'  : room.description,
                'nickname'     : room.users.nickname,
                'image_url'    : room.rooms_contents.first().thumbnails_url,
                'running_time' : (datetime.now() - room.created_at).seconds // 60,
            } for room in flatten(rooms)[OFFSET:OFFSET+LIMIT]
        ]

        # http://---:8000/rooms/search/category=roomname&keyword=키워드
        # 카테고리 - 방,컨텐츠,유저 이름 요청
        # 키워드 - keyword 요청
        # 필터 - 시청자 수, 스트리밍 시간, 공개 유/무 요청
        
        result = {}
        return JsonResponse({'result':result}, status=200)

'''
1. 요청
- room name
- content name
- nick name
- text (keyword)
- Category (유튜브, 넷플릭스)
- room name
- 실시간 시청자 수 (방 만들며 생기는 maximum)
- 플레이 리스트 갯수 이하
- 공개 or 비공개

2. 선택 사항에 맞춰 검색
- content name
- nick name

4. 필터
- Category (유튜브, 넷플릭스)
- 실시간 시청자 수 (방 만들며 생기는 maximum)
- 플레이 리스트 갯수 이하
- 공개 or 비공개

5. 출력 
- 영상 이름
- 방 이름
- 닉네임
- 스트리밍 시간 (10분 전)
- 시청자 수
- 사진
- 
'''

