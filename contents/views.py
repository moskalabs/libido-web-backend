import json, requests

from django.http       import JsonResponse
from django.conf       import settings
from django.views      import View
from json.decoder      import JSONDecodeError

from .models           import *


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
                'link_url'      : 'https://www.youtube.com/video/' + item['id']['videoId'],
                'title'         : item['snippet']['title'],
                'description'   : item['snippet']['description'],
                'image_url'     : item['snippet']['thumbnails']['medium']['url'],
                'channel_id'    : item['snippet']['channelId'],
                'channel_title' : item['snippet']['channelTitle'],
            } for item in items
        ]

        return JsonResponse({'message': result, 'page' : page}, status=200)