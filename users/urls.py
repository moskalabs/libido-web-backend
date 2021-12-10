from django.urls         import path
from .views              import *

app_name = 'users'
urlpatterns = [
    path("/sendsms", SendSMSView.as_view()),
    path("/signup", SignupView.as_view()),
    path("/signin", SigninView.as_view()),
    path("/sendemail", SendEmailView.as_view()),
    path("/resetpw", ResetPasswordView.as_view()),
]