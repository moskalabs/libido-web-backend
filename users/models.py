from django.db import models

from core.models    import TimeStampModel


class User(TimeStampModel):
    email              = models.EmailField(max_length=250, unique=True)
    password           = models.CharField(max_length=300)
    name               = models.CharField(max_length=30, null=True)
    nickname           = models.CharField(max_length=30, unique=True)
    phone_number       = models.CharField(max_length=30)
    profile_image_url  = models.URLField(max_length=2000, null=True)
    is_receive_email   = models.BooleanField(default=False)
    description        = models.TextField(null=True)
    day_of_birth       = models.CharField(max_length=30, null=True)
    nation             = models.CharField(max_length=30)
    login_method       = models.CharField(max_length=30, null=True)
    platform_id        = models.CharField(max_length=100, null=True)
    reset_token_number = models.CharField(max_length=30, null=True)
    user_histories     = models.ManyToManyField('rooms.Room', through="rooms.UserRoomHistory", related_name="users_histories")
    
    class Meta:
        db_table = 'users'


class Follow(TimeStampModel):
    users    = models.ForeignKey('user', on_delete=models.CASCADE, related_name='follow_by_users')
    followed = models.ForeignKey('user', on_delete=models.CASCADE, related_name='follow_by_followed')

    class Meta:
        db_table = 'follows'
        constraints = [
            models.UniqueConstraint(fields=['followed_id', 'users_id'], name='unique_follows')
        ]
