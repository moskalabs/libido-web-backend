from django.urls import path, include

urlpatterns = [
    path('contents', include('contents.urls')),
]
