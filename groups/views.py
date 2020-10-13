from django.shortcuts import render
from rest_framework.views import APIView
from profiles.models import StudentProfile
from rest_framework.generics import CreateAPIView
from groups.models import Group
from .serializers import *
from rest_framework.permissions import AllowAny
from profiles.models import StudentProfile
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from .permission import *
from .models import *
from notifications.models import sendNotification
from pfe import settings
from django.db.models import Q
from session.permissions import DepotDeProjet,ValidationDesProjet,ChoixDesProjet,Groupment,ResultasFinal




class CreateGr(APIView):
    #permission_classes=[IsStudent,AlreadyMemberInGroup,Groupment]
    permission_classes=[IsStudent,AlreadyMemberInGroup,]
    def post(self,request):
                student = StudentProfile.objects.get(user=request.user) 
                if student.have_group==False:
                        leader = StudentProfile.objects.get(user=request.user)
                        leader.have_group=True
                        serializer=GSereializer(data=request.data)
                        if serializer.is_valid(raise_exception=True):
                                leader = StudentProfile.objects.get(user=request.user)
                                serializer.save(leader=leader)
                                serializer.save()
                                student = StudentProfile.objects.get(user=request.user)
                                grp=Group.objects.get(leader=student)
                                grp.my_promo()
                                grp.save()
                                leader.my_group=grp
                                leader.have_group=True
                                leader.save()
                                title = grp.groupName + " created"
                                body = grp.groupName+" has been created succesfully"
                                channel = 'Groups'
                                event = 'GroupCreated'
                                sendNotification(request.user,title,body,channel,event)
                                return JsonResponse({"note":"Group Succesfuly Created",
                                        "status":"succes"},status=status.HTTP_200_OK)
                        else:
                                return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                else: return JsonResponse({"note":"you are already member in group"})

class Lookupmembers(APIView):
    #permission_classes=[IsStudent,Groupment]
    permission_classes=[IsStudent]
    def get(self,request,name):
        leader = StudentProfile.objects.get(user=request.user)
        promo_leader=leader.promo
        query=StudentProfile.objects.filter(promo=promo_leader)
        availaible=query.filter(Q(first_name__startswith = name) | Q(last_name__startswith = name), have_group=False)
        Serailizer=availaible_students(availaible,many=True)
        return JsonResponse(Serailizer.data,status=200,safe=False)




class Invitation(APIView):
    permission_classes=[IsStudent] ##Groupment
    def post(self,request):
        student = StudentProfile.objects.get(user=request.user)
        if student.have_group==True:
            return JsonResponse({"Note": "you already have a group"})
        else:
            serializer=handleInvite(data=request.data)
            if serializer.is_valid():
                groupName = serializer.data["grp"]
                accepted = serializer.data["accepted"]
                grp=Group.objects.get(groupName=groupName)
                invite=Invite.objects.filter(grp=grp).first()
                invite.accepted=accepted
                invite.save()
                number_of_members=grp.member_count()
                obj=Max.objects.get(id=1)
                max=obj.maxMembers
                if number_of_members >= max:
                    if invite.accepted==True:
                        invite.accepted=null
                        invite.save()
                    return JsonResponse({"Note": "Group Is Full"})
                else:
                    if invite.accepted==True:
                        student.have_group=True
                        student.save()
                        student.my_group=grp
                        student.save()
                        Invitations = Invite.objects.filter(member=student,grp=grp)
                        Invitations.delete() 
                        title = grp.groupName
                        body = 'you have been added to '+ grp.groupName
                        channel = 'Groups'
                        event = 'added'
                        sendNotification(student.user,title,body,channel,event)  
                        return JsonResponse({"note":"Member added"},status=200,safe=False)
                    else:
                        Invitations = Invite.objects.filter(member=student,grp=grp)
                        Invitations.delete() 
                        return JsonResponse({"note":"invitation refused"})
            else:
                return JsonResponse({'error':'bad request'},status=400)

class getInvites(APIView):
    permission_classes=[IsStudent,] #Groupment
    def get(self,request):
        student = StudentProfile.objects.get(user=request.user)
        query=Invite.objects.filter(member=student,accepted=None)
        Serailizer=getInvitations(query,many=True)
        return JsonResponse(Serailizer.data,status=200,safe=False)

class invite(APIView):
    permission_classes=[IsStudent,] #Groupment
    def post(self,request):
        leader = StudentProfile.objects.get(user=request.user)
        grp=Group.objects.get(leader=leader)
        number_of_members=grp.member_count()
        obj=Max.objects.get(id=1)
        max=obj.maxMembers
        if number_of_members >= max :
            return JsonResponse({"Note": "Group Is Full"})
        else:
            serializer=availaible_students(data=request.data)
            if serializer.is_valid():
                first_name=serializer.data["first_name"]
                last_name=serializer.data["last_name"]
                try:
                    student=StudentProfile.objects.get(first_name=first_name,last_name=last_name)
                except StudentProfile.DoesNotExist:
                    student=None
                if student:
                    i = Invite()
                    i.grp = grp
                    i.member = student
                    i.save()
                    title = grp.groupName
                    body = leader.__str__() + 'invited you to join his groupe '+ grp.groupName
                    channel = 'Groups'
                    event = 'invited'
                    sendNotification(student.user,title,body,channel,event)  
                    return JsonResponse({"note":"invitation sent"},status=200,safe=False)
                else:
                    return JsonResponse({"note":"This student is not availaible"})
            else:
                    return JsonResponse({'error':'bad request'},status=400)
       
class DeleteGroup(APIView):
    permission_classes=[IsStudent,IsGroupLeader,] #Groupment
    def delete(self,request):
        leader = StudentProfile.objects.get(user=request.user)
        grp=Group.objects.get(leader=leader)
        members=grp.all_members()
        grp.delete()
        title = 'your group was deleted succesfuly'
        body = 'your group was deleted by ' + leader.__str__()
        channel = 'Groups'
        event = 'GroupDeleted'
        for member in members :
            member.have_group=False
            sendNotification(member,title,body,channel,event)
        return JsonResponse({"Note":"Group Deleted"},status=200,safe=False)


class DeleteMember(APIView):
    permission_classes=[IsStudent,IsGroupLeader,] #Groupment
    def post(self,request):
                    student = StudentProfile.objects.get(user=request.user) 
#if student.have_group==False:
                    leader = StudentProfile.objects.get(user=request.user)
                    grp=Group.objects.get(leader=leader)
                    serializer=availaible_students(data=request.data)
                    if serializer.is_valid():
                        first_name=serializer.data["first_name"]
                        last_name=serializer.data["last_name"]
                        try:
                            student=StudentProfile.objects.get(first_name=first_name,last_name=last_name)
                        except StudentProfile.DoesNotExist:
                            student=None
                        MyGroupmembers=grp.all_members()
                        if student:
                                if  student in MyGroupmembers:
                                        student.have_group=False
                                        student.save()
                                        student.my_group=None
                                        student.save()
                                        title = grp.groupName
                                        body = 'you have been kicked from '+ grp.groupName
                                        channel = 'Groups'
                                        event = 'kicked'
                                        sendNotification(student.user,title,body,channel,event)                        
                                        return JsonResponse({"note":"Student Deleted"},status=200,safe=False)
                                else:
                                        return JsonResponse({"note":"This student is not in your group"})
                        else:
                                    return JsonResponse({"note":"This student does not exist"})
                    else:
                        return JsonResponse(serializer.errors,status=400)
                #else: return JsonResponse({"note":"you are already member in group"})

class AddToFiche(APIView):
    permission_classes = [IsGroupLeader,] #ChoixDesProjet
    def post(self, request):
        data = request.data
        student = StudentProfile.objects.get(user=request.user)
        print(student)
        group = Group.objects.get(leader=student)
        fiche = FicheDeVoeux()
        print(group)
        fiche.groupfiche = group
        choicelist=[]
        for key in data:
            post = Post.objects.get(title=data[key])
            choicelist.append(post)
        fiche.choices = choicelist
        fiche.my_promo()
        print(fiche)
        fiche.save()
        return JsonResponse({"Note": "la fiche has been created"})


class lookupposts(APIView):
    permission_classes=[IsStudent,] #ChoixDesProjet
    def get(self,request,name):
        leader = StudentProfile.objects.get(user=request.user)
        promo_leader=leader.promo
        query=Post.objects.filter(promo=promo_leader)
        availaible=query.filter(title__startswith = name)
        Serailizer=availaible_students(availaible,many=True)
        return JsonResponse(Serailizer.data,status=200,safe=False)

    
class GroupMembers(APIView):
    permission_classes=[IsStudent,] #Groupment
    def get(self, request):
        student = StudentProfile.objects.get(user=request.user)
        group = student.my_group
        members = group.all_members()
        serializer= grpmembers(members, many=True)
        return JsonResponse(serializer.data,status=200,safe=False)


class AddToFiche3CS(APIView):
    permission_classes = [IsGroupLeader,] #ChoixDesProjet
    def post(self, request):
        data = request.data
        student = StudentProfile.objects.get(user=request.user)
        group = Group.objects.get(leader=student)
        fiche = FicheDeVoeux()
        fiche.GroupeFiche = group
        choicelist=[]
        for key in data:
            post = Post.objects.get(title=data[key])
            choicelist.append(post)
        fiche.choices = choicelist
        fiche.save()
        return JsonResponse({"Note": "la fiche has been created"})


class finalResult(APIView):
    permissions_classes = [] #ResultasFinal
    def get(self,request):
        user=StudentProfile.objects.get(user=request.user)
        promo=user.promo
        fiches=FicheDeVoeux.objects.filter(promo=promo)
        serializer=finalResults(fiches,many=True)
        return JsonResponse(serializer.data,status=200,safe=False)
















