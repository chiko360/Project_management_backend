from django.shortcuts import render
from rest_framework.views import APIView
from profiles.models import StudentProfile
from rest_framework.generics import CreateAPIView
from groups.models import Group
from groups.serializers import *
from rest_framework.permissions import AllowAny
from profiles.models import StudentProfile
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from .permission import *
from .models import *
from notifications.models import sendNotification
from pfe import settings
import random
from django.views.generic import TemplateView
#from .forms import MyForm
from session.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.http import HttpResponse
from django.views import View
from pfe.settings import MAXMEMBERS,MAXCHOICES



def randome(promo):
    np = Post.objects.filter(promo=promo).count()  #######d<1 Probleme 
    nf = FicheDeVoeux.objects.filter(promo=promo).count() ###### filter by Promo
    if (nf == 0):
        return HttpResponse("no projects for "+ promo)
    else :
        obj=Max.objects.get(id=1)
        max=obj.maxChoices

        d = round(np/nf)
        queryFiche = FicheDeVoeux.objects.filter(promo=promo)
        queryPost = Post.objects.filter(promo=promo)
        l=list()
        for post in queryPost:
            l.append(post)
        for group in queryFiche:
            choosed_group = random.choice(queryFiche)
            print(choosed_group)
            print("maxCHOICES:",max)
            #for i in range(2): ###max choices of every Group
            for i in range(max):
                for j in reversed(range(len(l))):

                    print(j)
                    if ((l[j] == choosed_group.choices[i]) and (d >l[j].project_choice_count())):
                            choosed_group.selected_project = l[j]
                            choosed_group.save()
                            q1=queryFiche.exclude(groupfiche=choosed_group.groupfiche)
                            queryFiche=q1
                            print(queryFiche)
                            print("Done !")

                            if d <= l[j].project_choice_count():
                                title=l[j].title

                                l.pop()
                                print("Pooped")
                                break
                            else:
                                continue
                            break
                    else:
                        continue
                    
                    
                if choosed_group.selected_project:
                    break
                else:
                    continue
                
                
                
        if (queryFiche != None and queryPost == None):
            print('i; here if')
            queryPost2 = Post.objects.filter(approved=True)
            for group in queryFiche:
                choosed_group = random.choice(queryFiche)
                for i in range(MAXCHOICES):
                    for post in queryPost2:
                        if post == choosed_group.choices[i]:
                                choosed_group.selected_project = post
                                choosed_group.save()
                                queryFiche.exclude(groupfiche=group.groupfiche)
                                title=post.title
                                queryPost2.exclude(title=title)
                                break
                        else:
                                continue
                    break
                break
            return HttpResponse('result')

        else:
            return HttpResponse('result')
def leader_mark(promo):
    np =Post.objects.filter(promo=promo).count()
    nf = FicheDeVoeux.objects.filter(promo=promo).count()
    if (nf == 0):
        return HttpResponse("no projects for "+ promo)
    else :
        d = round(np/nf)
        print(d)
        queryFiche = FicheDeVoeux.objects.filter(promo=promo)
        queryGroup=Group.objects.filter(promo1=promo)
        queryPost = Post.objects.filter(promo=promo)
        listLeaders=list()
        for group in queryGroup:
            listLeaders.append(group.leader)
            #print(group.leader)
            #print(group.leader)
            ####ORRDER LISTLEADERS BY marks
        #print(len(listLeaders))
        listLeaders.sort(key=lambda leader: leader.marks)
        print(listLeaders)
            
        for i in reversed(range(len(listLeaders))):
            choosed_group=Group.objects.get(leader=listLeaders[i])
            
            group_fiche=FicheDeVoeux.objects.get(groupfiche=choosed_group)
            obj=Max.objects.get(id=1)
            max=2
            for i in range(max): ##### 2 =variable of max choices
                for post in queryPost:
                    print("A")
                    if post == group_fiche.choices[i] and 3 > post.project_choice_count():
                            
                            group_fiche.selected_project = post
                            group_fiche.save()
                            print("done!")
                            #queryFiche.exclude(groupfiche=group.groupfiche)
                            listLeaders.pop()
                            if 3 <= post.project_choice_count():
                                #queryPost.exclude(groupfiche=group.groupfiche)
                                print("here!!")
                                title=post.title
                                queryPost.exclude(title=title)
                                break
                            else:
                                continue
                            break
                    else:
                        continue
                if group_fiche.selected_project:
                    break
                else:
                    continue
        if (queryFiche != None and queryPost == None):
            for i in reversed(range(len(listLeaders))):
                choosed_group=Group.objects.get(leader=listLeaders[i])
                group_fiche=FicheDeVoeux.objects.get(GroupFiche=choosed_group)
                for i in range(MAXCHOICES):
                    for post in queryPost:
                        if post == group_fiche.choices[i] and 3 > post.project_choice_count():
                                group_fiche.selected_project = post
                                queryFiche.exclude(groupfiche=group.groupfiche)
                                print("done!")
                                listLeaders.pop()
                                if 3 <= post.project_choice_count():
                                    title=post.title
                                    queryPost.exclude(title=title)
                                    #queryPost.exclude(po
                                    break
                                else:
                                    continue
                    break
                break
            return HttpResponse('result')
        else:
            return HttpResponse('result')
def group_mark(promo):
            
    np = Post.objects.filter(promo=promo).count()
    nf = FicheDeVoeux.objects.filter(promo=promo).count()
    d = round(np/nf)
    queryFiche = FicheDeVoeux.objects.filter(promo=promo)
    queryGroup=Group.objects.filter(promo1=promo)
    queryPost = Post.objects.filter(promo=promo)
    groupsList=list()
    for group in queryGroup:
        groupsList.append(group)
        
        ####ORRDER Groups BY marks
    groupsList.sort(key=lambda group: group.group_marks())
    
    
    print(len(groupsList))
    for i in reversed(range(len(groupsList))):
        #leader=StudentProfile.objects.get()
        choosed_group=Group.objects.get(leader=groupsList[i].leader)
        group_fiche=FicheDeVoeux.objects.get(groupfiche=choosed_group)
        for i in range(MAXCHOICES):
            for post in queryPost:
                if post == group_fiche.choices[i] and d > post.project_choice_count():
                        group_fiche.selected_project = post
                        group_fiche.save()
                        print("Done!")
                        #queryFiche.exclude(groupfiche=group.groupfiche)
                        groupsList.pop()
                        if d <= post.project_choice_count():
                            #queryPost.exclude(groupfiche=group.groupfiche)
                            title=post.title
                            queryPost.exclude(title=title)
                            break
                        else:
                            continue
                        break
                else:
                    continue
            if group_fiche.selected_project:
                break
            else:
                continue
    if (queryFiche != None and queryPost == None):
        for i in reversed(range(len(groupList))):
            choosed_group=Group.objects.get(leader=groupList[i])
            group_fiche=FicheDeVoeux.objects.get(GroupFiche=choosed_group)
            for i in range(MAXCHOICES):
                for post in queryPost:
                    if post == group_fiche.choices[i] and d > post.project_choice_count():
                            group_fiche.selected_project = post
                            #queryFiche.exclude(groupfiche=group.groupfiche)
                            groupList.pop()
                            if d <= post.project_choice_count():
                                #queryPost.exclude(groupfiche=group.groupfiche)
                                queryPost.exclude(post)
                                break
                            else:
                                continue
                    else:
                        continue
                break
            break
        return HttpResponse('result')
    else:
        return HttpResponse('result')

def randome1(promo):
    posts = Post.objects.filter(promo=promo)#######d<1 Probleme 
    fiches = FicheDeVoeux.objects.filter(promo=promo)
    for fiche in fiches:
        choosed_group = random.choice(posts)
        fiche.selected_project=choosed_group
        fiche.save()
    return HttpResponse('result')