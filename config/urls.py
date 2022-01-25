from django.urls import path, include
from django.conf.urls import include, url
from django.contrib import admin


from drf_yasg import openapi
from drf_yasg.views import get_schema_view

import users.v2_urls as v2_user_urls


schema_view = get_schema_view(
    openapi.Info(
        title="Libido Service API",
        default_version="v1",
        description="v1",
        terms_of_service="Libido",
        contact=openapi.Contact(email="help@libodo.co.kr"),
        license=openapi.License(name="BSD License"),
    ),
    # validators=["flex", "ssv"],
    public=True,
    # permission_classes=(RetriveListOnly,),
)

urlpatterns = [
    url(r"^v2/", include(v2_user_urls)),
    path("contents", include("contents.urls")),
    path("users", include("users.urls")),
    path("rooms", include("rooms.urls")),
    # url(r"", include("chats.urls")),
    path("libido_test_admin/", admin.site.urls),
]


urlpatterns += [
    url(
        r"^libido_v1_swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^libido_v1_swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^libido_v1_redocs/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
