from django.conf.urls import include, url
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from contents.views import ContentViewSet


content_router = DefaultRouter(trailing_slash=False)
content_router.register(r"contents", ContentViewSet, basename="contents")

urlpatterns = [
    url(r"^", include(content_router.urls)),
]
