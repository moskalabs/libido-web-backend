from django.urls         import path
from .views              import SendSMSView

app_name = 'users'
urlpatterns = [
    path("/sendsms", SendSMSView.as_view()),
]