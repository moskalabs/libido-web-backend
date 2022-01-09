from django.urls import path, include
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    path("contents", include("contents.urls")),
    path("users", include("users.urls")),
    path("rooms", include("rooms.urls")),
    url(r"", include("chats.urls")),
    # path("libido_test_admin/", admin.site.urls),
]
