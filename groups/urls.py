from django.urls import path
from django.conf.urls import url
from .views import *
from .views2 import *

urlpatterns = [
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



    path("teammarks/",basedOnTeamMarks),
    path("leader/",BasedOnLeaderMarks),
    path("random/",RandomPorjects),
    path("finalresults/",finalResult.as_view()),
    
]