from django.urls         import path
from .views              import *

app_name = 'users'
urlpatterns = [
    path("/signup", SignupView.as_view()),
]