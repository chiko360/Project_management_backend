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
class IsGroupLeader(permissions.BasePermission):
    message="You are already group leader"
    def has_permission(self,request,view):
        student = StudentProfile.objects.get(user=request.user) 
        try:
            group_leader=Group.objects.get(leader=student)
        except Group.DoesNotExist:
            group_leader=None
        
        if not group_leader:
            return False
        else:
            return True


class IsNotGroupLeader(permissions.BasePermission):
    message="You are already group leader"
    def has_permission(self,request,view):
        student = StudentProfile.objects.get(user=request.user) 
        try:
            group_leader=Group.objects.get(leader=student)
        except Group.DoesNotExist:
            group_leader=None
        
        if not group_leader:
            return True
        else:
            return False

class AlreadyMemberInGroup(permissions.BasePermission):
    message="You are already a member in a group"
    def has_permission(self,request,view):
        try:
            student = StudentProfile.objects.get(user=request.user) 
        except StudentProfile.DoesNotExist:
            student=None
        
        if student.have_group==True:
            return False
        else:
            return True    

class IsStudent(permissions.BasePermission):
    message = 'Only students have permission'
    def has_permission(self,request,view):
        try:
            Profile= StudentProfile.objects.get(user=request.user) 
        except StudentProfile.DoesNotExist:
            Profile = None
        if Profile:
            return True
        else:
            return False

class IsTeacher(permissions.BasePermission):
    
    message = 'Only Teacher have permisson'
    def has_permission(self,request,view):
        try:
            Profile= TeacherProfile.objects.get(user=request.user) 
        except TeacherProfile.DoesNotExist:
            Profile = None
        if Profile:
            return True
        else:
            return False

        













