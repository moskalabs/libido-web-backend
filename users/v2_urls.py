from django.conf.urls import include, url
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from users.views import UserViewSet


user_router = DefaultRouter(trailing_slash=False)
user_router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    url(r"^", include(user_router.urls)),
]
