from django.db import models
from posts.models import Post
from picklefield.fields import PickledObjectField
import jsonfield
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid


class Group(models.Model):

    leader=models.OneToOneField("profiles.StudentProfile", on_delete=models.SET_NULL,related_name='group_leaders',null=True)
    groupName=models.CharField(max_length=255)
    promo1=models.CharField(blank=True,null=True,max_length=9)

    def __str__(self):
        return self.groupName

    def leaderName(self):
        return self.leader.__str__()
    
    def member_count(self):
        return self.members.count()+1
    
    def all_members(self):
        return self.members.all()

    def group_marks(self):
        members=self.all_members()
        moyenne=0
        moyenne=moyenne+self.leader.marks
        for member in members:
            moyenne=moyenne+member.marks
        return moyenne/self.member_count()
    def my_promo(self):
         self.promo1=self.leader.promo


class FicheDeVoeux(models.Model):
    choices = PickledObjectField()
    groupfiche=models.OneToOneField(Group,on_delete=models.SET_NULL,blank=True, null=True)
    selected_project = models.ForeignKey(Post, on_delete=models.SET_NULL, related_name="selected",null=True,blank=True)
    promo=models.CharField(blank=True,null=True,max_length=9)
    
    def my_promo(self):
        self.promo=self.groupfiche.leader.promo

    def __str__(self):
        if self.groupfiche!=None:
            return self.groupfiche.groupName
        else :return 'no name';

class Invite(models.Model):
    grp = models.ForeignKey(Group,on_delete=models.CASCADE,blank=True, null=True)
    member = models.ForeignKey("profiles.StudentProfile", on_delete=models.SET_NULL,related_name='invited_member',null=True)
    accepted = models.BooleanField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.member.__str__()


class Max(models.Model):
    maxChoices=models.PositiveIntegerField(blank=True, null=True)
    maxMembers=models.PositiveIntegerField(blank=True, null=True)




    

    




    

    




    
