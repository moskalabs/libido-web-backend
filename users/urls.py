from django.urls         import path
from .views              import SendSMSView, SignupView

app_name = 'users'
urlpatterns = [
    path("/sendsms", SendSMSView.as_view()),
    path("/signup", SignupView.as_view())
]