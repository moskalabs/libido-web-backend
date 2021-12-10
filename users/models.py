from django.db import models

from core.models    import TimeStampModel


class User(TimeStampModel):
    name               = models.CharField(max_length=30, default='')
    day_of_birth       = models.CharField(max_length=30, default='')
    nation             = models.CharField(max_length=30, null=True)
    email              = models.EmailField(max_length=250, unique=True)
    password           = models.CharField(max_length=300, null=True)
    phone_number       = models.CharField(max_length=30)
    nickname           = models.CharField(max_length=30, unique=True)
    profile_image_url  = models.URLField(max_length=2000, null=True)
    login_method       = models.CharField(max_length=30, null=True)
    platform_id        = models.CharField(max_length=30, null=True)
    description        = models.TextField(null=True)
    reset_token_number = models.CharField(max_length=30, null=True)
    user_histories     = models.ManyToManyField('rooms.Room', through="rooms.UserRoomHistory", related_name="users_histories")
    
    class Meta:
        db_table = 'users'


class Follow(models.Model):
    users    = models.ForeignKey('user', on_delete=models.CASCADE, related_name='follow_by_users')
    followed = models.ForeignKey('user', on_delete=models.CASCADE, related_name='foolow_by_followed')

    class Meta:
        db_table = 'follows'
