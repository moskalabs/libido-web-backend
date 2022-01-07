from django.urls import path
from .views import *

app_name = "users"
urlpatterns = [
    path("/emailcheck", EmailDuplicateCheckView.as_view()),
    path("/nicknamecheck", NicknameDuplicateCheckView.as_view()),
    path("/signup", SignupView.as_view()),
    path("/signin", SigninView.as_view()),
    path("/signupemail", SignupSendEmailView.as_view()),
    path("/resetemail", ResetPasswordSendEmailView.as_view()),
    path("/resetpw", ResetPasswordView.as_view()),
    path("/google/login", GoogleSignInView.as_view()),
    path("/naver/login", NaverSignInView.as_view()),
    path("/follows", UserFollowView.as_view()),
    path("/history", UserHistoryView.as_view()),
    path("/profile", UserProfileView.as_view()),
]
