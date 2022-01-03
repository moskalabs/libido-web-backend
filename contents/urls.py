from django.urls import path
from .views import SearchContentView, ContentListView

urlpatterns = [
    path("", ContentListView.as_view()),
    path("search", SearchContentView.as_view()),
]

