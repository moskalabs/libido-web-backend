from django.db import models

from core.models    import TimeStampModel

class Content(TimeStampModel):
    title              = models.CharField(max_length=100)
    content_link_url   = models.URLField(max_length=2000)
    thumbnails_url     = models.URLField(max_length=2000)
    running_time       = models.CharField(max_length=50, null=True)
    view_count         = models.PositiveIntegerField(null=True)
    like_count         = models.PositiveIntegerField(null=True)
    dislike_count      = models.PositiveIntegerField(null=True)
    channel_id         = models.CharField(max_length=50, null=True)
    channel_title      = models.CharField(max_length=50, null=True)
    published_at       = models.CharField(max_length=50, null=True)
    content_categories = models.ForeignKey('ContentCategory', on_delete=models.CASCADE, related_name='contents')
    content_tags       = models.ManyToManyField('Tag', through="ContentTag", related_name="contents")
    
    class Meta:
        db_table = 'contents'


class ContentCategory(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'content_categories'


class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'tags'


class ContentTag(models.Model):
    contents = models.ForeignKey('Content', on_delete=models.CASCADE)
    tags     = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'content_tags'

