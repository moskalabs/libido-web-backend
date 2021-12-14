import json

from django.http       import JsonResponse
from django.views      import View
from django.db.models  import Q
from json.decoder      import JSONDecodeError

from .models           import *
from users.models   import *
from contents.models   import *
from core.views        import login_required

class RoomListView(View):
    @login_required
    def get(self, request):
        category = request.GET.get('category')
        user     = request.user
        OFFSET   = int(request.GET.get('offset', 0))
        LIMIT    = int(request.GET.get('display', 8))

        q = Q()
        ordering_priority = []

        if category == 'customize':
            hitoryies = user.user_histories.all()

            if hitoryies:
                contents  = [history.rooms_contents.all() for history in hitoryies]
                tag_list  = set([tag.id for content in contents for tag in content[0].content_tags.all()])
                
                sort = '-view_count'
                ordering_priority.append(sort)
                q.add(Q(content_tags__id__in = tag_list), q.AND)
            else:
                sort = ['?', '-view_count']
                ordering_priority.extend(sort)

        if category == 'popular':
            sort = '-created_at'
            ordering_priority.append(sort)

        contents = Content.objects.filter(q).select_related('content_categories').order_by(*ordering_priority).distinct()
        rooms    = [content.rooms.all() for content in contents if content.rooms.all().exists()][OFFSET:OFFSET+LIMIT]

        result = [
            {   
                'id'            : room[0].id,
                'category'      : room[0].rooms_contents.first().content_categories.name,
                'is_public'     : room[0].is_public,
                'password'      : room[0].password,
                'link_url'      : room[0].rooms_contents.first().content_link_url,
                'title'         : room[0].title,
                'title'         : room[0].description,
                'nickname'      : room[0].users.nickname,
                'image_url'     : room[0].rooms_contents.first().thumbnails_url,
                'published_at'  : room[0].created_at,
            } for room in rooms
        ]

        return JsonResponse({'message': result}, status=200)