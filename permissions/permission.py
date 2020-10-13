from rest_framework import permissions
from .models import Group
from profiles.models import StudentProfile,TeacherProfile
#Delete_members
#List_groups_members
#Delete_group
#Create_Group
#List_Availaible_Members
#add_member
#have_group


#AlreadyCreatedAgroup
class depotDeProjet(permissions.BasePermission):
    message="depot de projet"
    def has_permission(self,request,view):
        permission = StudentProfile.objects.get(user=request.user) 
        try:
            group_leader=Group.objects.get(leader=student)
        except Group.DoesNotExist:
            group_leader=None
        
        if not group_leader:
            return False
        else:
            return True