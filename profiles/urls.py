from django.conf.urls import url
from django.urls import path
from .views import *


urlpatterns = [
    path('getgroup/', getGroup.as_view()),
    url(r'^teacher/', TeacherProfileView.as_view()),
    url(r'^student/', StudentProfileView.as_view()),
    ]