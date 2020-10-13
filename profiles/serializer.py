from .models import *
from rest_framework import serializers

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherProfile
        fields = ("id", "first_name", "last_name")


class HaveGroup(serializers.ModelSerializer):
    grp = serializers.SerializerMethodField("GrpName")
    leader = serializers.SerializerMethodField("isleader")
    leaderName = serializers.SerializerMethodField("nleader")
    #username = serializers.CharField(read_only=True, source="user.username")
    class Meta:
        model=StudentProfile
        fields=['grp','leader','leaderName']
    
    def GrpName(self,obj):
        if obj.my_group!=None:
            grp= obj.my_group.groupName
            return grp
        else:
            a=""
            return a

    def isleader(self,obj):
        if obj.my_group!=None:
            l = obj.my_group.leader
            return (l==obj)
        else:
            return False
    
    def nleader(self,obj):
        if obj.my_group==None:
            a=""
            return a
        else:
            l=obj.my_group.leader.first_name +" "+ obj.my_group.leader.last_name
            return l

