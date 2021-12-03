from django.urls import path
from .views import SearchContentView

urlpatterns = [
    path('/search', SearchContentView.as_view()),
]