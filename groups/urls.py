from django.urls import path
from django.conf.urls import url
from .views import *


urlpatterns = [
    path("finalresults/final/",finalResult.as_view()),
    path("handleinvite/",Invitation.as_view()),
    path("invitations/",getInvites.as_view()),
    path("creategroup/",CreateGr.as_view()),
    path("deletegroup/",DeleteGroup.as_view()),
    path("addmember/",invite.as_view()),
	path("deletemember/",DeleteMember.as_view()),
    path("getMembers/",GroupMembers.as_view()),
    path("Lookupmembers/",Lookupmembers.as_view()),
    path("lookupposts/",lookupposts.as_view()),
    path("addtofiche/",AddToFiche.as_view()),
    path('members/',GrpMembers.as_view()),
    path("finalresults/",finalResult.as_view()),
    path("fmembers/",GrpMembers.as_view()),
    path("getMax/",getMax.as_view()),
    
    
]