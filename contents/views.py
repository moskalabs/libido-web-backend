import json, requests

from django.http       import JsonResponse
from django.conf       import settings
from django.views      import View
from django.db.models  import Q

from .models           import *
from users.models      import *
from core.utils        import login_required


class SearchContentView(View):
    def get(self, request):
        keyword = request.GET.get('keyword')
        OFFSET  = request.GET.get("page")
        LIMIT   = int(request.GET.get("limit", 50))

        search_url = 'https://www.googleapis.com/youtube/v3/search'
        
        params = {
            'q'             : keyword,
            'part'          : 'snippet',
            'key'           : settings.YOUTUBE_DATA_API_KEY,
            'regionCode'    : 'KR',
            'order'         : 'relevance',
            'maxResults'    : LIMIT,
            'type'          : 'video',
            'pageToken'     : OFFSET
        }

        data  = requests.get(search_url, params=params).json()
        page  = data['nextPageToken']
        items = data['items']

        result = [
            {
                'link_url'      : 'https://www.youtube.com/embed/'+item['id']['videoId'],
                'title'         : item['snippet']['title'],
                'image_url'     : item['snippet']['thumbnails']['medium']['url'],
                'channel_id'    : item['snippet']['channelId'],
                'channel_title' : item['snippet']['channelTitle'],
                'published_at'  : item['snippet']['publishedAt'],
            } for item in items
        ]

        return JsonResponse({'message': result, 'page' : page}, status=200)


class ContentListView(View):
    @login_required
    def get(self, request):
        category = request.GET.get('category')
        OFFSET   = int(request.GET.get('offset', 0))
        LIMIT    = int(request.GET.get('display', 8))

        q = Q()
        ordering_priority = []

        if category == 'customize':
            hitoryies = request.user.user_histories.all().prefetch_related('rooms_contents', 'rooms_contents__content_tags')

            if hitoryies:
                sort = '-view_count'
                ordering_priority.append(sort)
                
                tag_list = set([tags.id for history in hitoryies for content in history.rooms_contents.all() for tags in content.content_tags.all()])
                q.add(Q(content_tags__id__in = tag_list), q.AND)

            else:
                sort = ['?', '-view_count']
                ordering_priority.extend(sort)
        
        if category == 'popular':
            sort = '-created_at'
            ordering_priority.append(sort)

        contents = Content.objects.filter(q).select_related('content_categories').order_by(*ordering_priority).distinct()[OFFSET:OFFSET+LIMIT]
        
        result = [
            {   
                'id'            : content.id,
                'category'      : content.content_categories.name,
                'link_url'      : content.content_link_url,
                'title'         : content.title,
                'image_url'     : content.thumbnails_url,
                'channel_id'    : content.channel_id,
                'channel_title' : content.channel_title,
                'running_time'  : content.running_time,
                'view_count'    : content.view_count,
                'published_at'  : content.published_at,
            } for content in contents
        ]

        return JsonResponse({'message': result}, status=200)