from django.conf.urls import include, url
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from users.views import FollowViewSet


follow_router = DefaultRouter(trailing_slash=False)
follow_router.register(r"followers", FollowViewSet, basename="follow")

urlpatterns = [
    url(r"^", include(follow_router.urls)),
]
