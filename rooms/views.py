import functools

from os       import error, lseek
from datetime import datetime
from tokenize import Name

from django.http                import JsonResponse
from django.views               import View
from django.db.models           import Q
from django.contrib.admin.utils import flatten

from rooms.models      import *
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
        여러 컨텐츠로 만들어진 방을 방, 컨텐츠, 유저 이름을 통해
        검색하는 기능
        - 방 검색 기능은 socket 통신을 통해 구현 될 예정,
        역량이 부족하여 socket 구현 및 제어 불가능.
        (Room table의 maximum_limit, status 임시 컬럼 생성,
        Room table을 현재 진행중인 방으로 취급 함.)
        현재는 mysql을 통해 만들어진 기능
        socket 통신이 가능하면 socket을 통해 실시간으로 정보가 바뀔 것
        '''
        try:
            where         = request.GET.get('where',None)
            keyword       = request.GET.get('keyword','')
            maximum_limit = request.GET.get('maximum_limit','500')
            playlists     = request.GET.get('playlists','20')
            public        = request.GET.get('public',True)
            OFFSET        = int(request.GET.get('offset',0))
            LIMIT         = int(request.GET.get('display',12))

            q = Q()

            if where == 'rooms':
                FILTERS = {
                    'keyword'       : Q(title__icontains=keyword),
                    'maximum_limit' : Q(maximum_limit__lte=maximum_limit),
                    'public'        : Q(is_public=public)
                }

            if where == 'contents':
                FILTERS = {
                    'keyword'       : Q(roomcontent__contents__title__icontains=keyword),
                    'maximum_limit' : Q(maximum_limit__lte=maximum_limit),
                    'public'        : Q(is_public=public)
                }

            if where == 'nickname':
                FILTERS = {
                    'keyword'       : Q(users_id__nickname__icontains=keyword),
                    'maximum_limit' : Q(maximum_limit__lte=maximum_limit),
                    'public'        : Q(is_public=public)
                }

            sort        = functools.reduce(lambda q1, q2: q1&q2, [FILTERS.get(key, Q()) for key in request.GET.keys()])
            sort_rooms  = [room for room in [room_set for room_set in\
                Room.objects.filter(sort).prefetch_related('rooms_contents').distinct()]\
                if room.rooms_contents.count() <= int(playlists)]
            
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
                    # 'running_time' : (datetime.now() - room.created_at).seconds // 60,
                    # 설정 시간이 안맞음 (UTC /= ASIS/Seoul)
                } for room in flatten(sort_rooms)[OFFSET:OFFSET+LIMIT]
            ]

            return JsonResponse({'keyword':result}, status=200)

        except NameError:
            return JsonResponse({'message':'UNKNOWN NAME'}, status=404)
        
        except TypeError:
            return JsonResponse({'message':'INVALID INITIALVALUE'}, status=404)