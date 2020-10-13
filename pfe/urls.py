from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from users.urls import *
from profiles.urls import *
from users.views import *
from groups.views import *
from notifications.views import *

admin.site.site_header = "Gestion des Projet ESI SBA"
admin.site.site_title = "ESI-SBA"
admin.site.index_title = "Gestion des Projet"

urlpatterns = [
	path("members/<name>/",Lookupmembers.as_view(),name='lookup'),
	path('', HomeView),
    path('admin/', admin.site.urls),
	path('auth/', include('users.urls')),
	path('profiles/', include('profiles.urls')),
	path('posts/',include('posts.urls')),
	path('groups/',include('groups.urls')),
	path('api/pusher/auth', PusherAuthView.as_view()),
	path('api/fiche/', AddToFiche.as_view()),
	path('api/notifications/', UnseenNotifications.as_view()),
	


	
]
