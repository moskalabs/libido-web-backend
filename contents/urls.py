from django.urls import path
from .views import SearchContentView, ContentListView

urlpatterns = [
    path("/search", SearchContentView.as_view()),
    path("", ContentListView.as_view()),
]
