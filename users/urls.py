from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'login/', UserLoginView.as_view()),
    url(r'change_password/',ChangePwView.as_view()),
    ]
