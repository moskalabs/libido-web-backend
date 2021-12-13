import requests
from datetime        import datetime

from django.conf     import settings

from contents.models import Content, ContentCategory, Tag, ContentTag
    
def popular_videos_get_youtube_api():
    search_url = 'https://www.googleapis.com/youtube/v3/videos'
        
    params = {
        'part'       : 'snippet,statistics,player,contentDetails,topicDetails',
        'chart'      : 'mostPopular',
        'regionCode' : 'KR',
        'maxResults' : 50,
        'key'        : settings.YOUTUBE_DATA_API_KEY,
    }

    data  = requests.get(search_url, params=params).json()
    items = data['items']
    
    youtube_obj, created = ContentCategory.objects.get_or_create(name = 'youtube')
    netflix_obj, created = ContentCategory.objects.get_or_create(name = 'netflix')
    watcha_obj, created  = ContentCategory.objects.get_or_create(name = 'watcha')

    for item in items:
        obj = Content.objects.create(
            title                 = item['snippet']['title'],
            content_link_url      = 'https://www.youtube.com/embed/' + item['id'],
            thumbnails_url        = item['snippet']['thumbnails']['medium']['url'],
            running_time          = item['contentDetails']['duration'][2:],
            view_count            = item['statistics'].get('viewCount'),
            like_count            = item['statistics'].get('likeCount'),
            dislike_count         = item['statistics'].get('dislikeCount'),
            channel_id            = item['snippet']['channelId'],
            channel_title         = item['snippet']['channelTitle'],
            published_at          = item['snippet']['publishedAt'],
            content_categories_id = youtube_obj.id,
        )
        if item.get('topicDetails'):
            tags = item['topicDetails']['topicCategories']
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(name = tag.split('/')[-1])
                ContentTag.objects.create(
                    contents_id = obj.id,
                    tags_id     = tag_obj.id
                )

    print(f'{datetime.now()} : {len(items)} data created')