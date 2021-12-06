from django.urls         import path
from .views              import SendSMSView, SignupView, SigninView

app_name = 'users'
urlpatterns = [
    path("/sendsms", SendSMSView.as_view()),
    path("/signup", SignupView.as_view()),
    path("/signin", SigninView.as_view()),
]