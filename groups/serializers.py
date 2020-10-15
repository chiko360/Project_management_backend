from rest_framework import serializers
from .models import *
from profiles.models import StudentProfile


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields=['groupName','group_members']

class GSereializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=['groupName']


class availaible_students(serializers.ModelSerializer):
    class Meta:
        model=StudentProfile
        fields=["first_name","last_name"]

class availaible_posts(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=["title"]

class grpmembers(serializers.ModelSerializer):
    class Meta:
        model=StudentProfile
        fields=["first_name","last_name","gender","birth_date"]

class fiche_de_voeux(serializers.ModelSerializer):
    class Meta:
        model=FicheDeVoeux
        fields=["choices"]

class handleInvite(serializers.Serializer):
    grp = serializers.CharField(max_length=200)
    accepted = serializers.BooleanField()

class getInvitations(serializers.ModelSerializer):
    grp = serializers.SerializerMethodField("grp_name")
    class Meta:
        model=Invite
        fields=["grp",'timestamp','accepted']
    
    def grp_name(self,obj):
            grp= obj.grp.__str__()
            return grp




class finalResults(serializers.ModelSerializer):
    groupfiche = serializers.SerializerMethodField("grp_name")
    selected_project =serializers.SerializerMethodField("project_selected")
    teacher_profile =serializers.SerializerMethodField("teacher")

    class Meta:
        model=FicheDeVoeux
        fields=["groupfiche",'selected_project',"teacher_profile"]
    
    def grp_name(self,obj):
            grp= obj.groupfiche.__str__()
            return grp

    def project_selected(self,obj):
        project=obj.selected_project.__str__()
        return project


    def teacher(self,obj):
        post=obj.selected_project
        if post !=None :
            teacher=post.user.first_name +" "+post.user.last_name
            return teacher
        else : return;

class GroupName(serializers.Serializer):
    grp = serializers.CharField(max_length=200)

class members(serializers.Serializer):
    first_name = serializers.SerializerMethodField("first_name")
    last_name =serializers.SerializerMethodField("last_name")
    
    def first_name(self,obj):
            grp= obj.groupfiche.__str__()
            return grp


