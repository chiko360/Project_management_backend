from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
	###STudent

	path('edit/<int:id>/',PostToEditView.as_view()), ##### /something ######## edited

	path("createpost/student/",createPostStudent.as_view()),	#### createpost for student
	path("studentprojects/",PostStudent.as_view()),          #### My posts as Student
	path('',PostListView.as_view(),name='list_posts'),#### list projects for student
	url(r'^(?P<title>[\w-]+)/$',PostDetailAPIView.as_view(),name='detail_posts'),

		###Teacher
	

	path('addpost/teacher/',create,name='create_post'), ### Create post for teacher ###### changment
	path('myprojects/teacher/',TeacherPostView.as_view(),name='teacher_view'), ### Teacher Projects
	url(r'^(?P<pk>[\d+]+)/edit/$',PostUpdate,name='update_posts'),  ###post update for teacher
	url(r'^(?P<pk>[\d+]+)/delete/$',PostDelete,name='delete_post'), ### post delete for teeacher
	#path('addpoststudent/',createPostStudent.as_view()),
	


	############ 3CS #############
	
	url(r'^(?P<pk>[\d+]+)/editpost/$',UpdatePostStudent.as_view(),name='update_posts'),
	url(r'^(?P<pk>[\d+]+)/deletepost/$',DeletePostStudent.as_view(),name='delete_post'),

]