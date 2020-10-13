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

class MyView(View):
    def post(self, request):
        
        if request.method == "POST ":
            a=request.POST
            print(a)
            return HttpResponse('result')

        else:
            return  HttpResponse('False')

        

       

################################################
def RandomPorjects(request):
    if request.method=='POST':
        promo=request.data['promo']
        np = Post.objects.filter(promo=promo).count()  #######d<1 Probleme 
        nf = FicheDeVoeux.objects.filter(promo=promo).count() ###### filter by Promo
        d = round(np/nf)
        queryFiche = FicheDeVoeux.objects.filter(promo=promo)
        queryPost = Post.objects.filter(promo=promo)
        l=list()
        for post in queryPost:
            l.append(post)
        for group in queryFiche:
            choosed_group = random.choice(queryFiche)
            print(choosed_group)
            for i in range(2): ###max choices of every Group
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
            queryPost2 = Post.objects.filter(approved=True)
            for group in queryFiche:
                choosed_group = random.choice(queryFiche)
                for i in range(5):
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
            return JsonResponse({"if":"if"},status=200)
        
        else:
            return  JsonResponse({"else":"else"},status=200)

def BasedOnLeaderMarks(APIView):
    if request.method=='POST':
        promo=request.data["promo"]
        np =Post.objects.filter(promo=promo).count()
        nf = FicheDeVoeux.objects.filter(promo=promo).count()
        d = round(np/nf)
        print(d)
        queryFiche = FicheDeVoeux.objects.filter(promo=promo)
        queryGroup=Group.objects.filter(promo=promo)
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
            print(listLeaders[i])
            group_fiche=FicheDeVoeux.objects.get(groupfiche=choosed_group)
            for i in range(2): ##### 2 =variable of max choices
                for post in queryPost:
                    print(i)
                    if post == group_fiche.choices[i] and d > post.project_choice_count():
                            print(post.project_choice_count())
                            group_fiche.selected_project = post
                            group_fiche.save()
                            print("done!")
                            #queryFiche.exclude(groupfiche=group.groupfiche)
                            listLeaders.pop()
                            if 2 <= post.project_choice_count():
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
                for i in range(5):
                    for post in queryPost:
                        if post == group_fiche.choices[i] and d > post.project_choice_count():
                                group_fiche.selected_project = post
                                queryFiche.exclude(groupfiche=group.groupfiche)
                                listLeaders.pop()
                                if d <= post.project_choice_count():
                                    title=post.title
                                    queryPost.exclude(title=title)
                                    #queryPost.exclude(post)

                                    break
                                else:
                                    continue
                    break
                break
            return JsonResponse({"if":"if"},status=200)   
        else:
            return JsonResponse({"else":"else"},status=200  )
###########prblm if d<1


def basedOnTeamMarks(APIView):
    if request.method=='POST':
        promo = request.data['promo']
        np = Post.objects.filter(promo=promo).count()
        nf = FicheDeVoeux.objects.filter(promo=promo).count()
        d = round(np/nf)
        queryFiche = FicheDeVoeux.objects.filter(promo=promo)
        queryGroup=Group.objects.filter(promo=promo)
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
            for i in range(2):
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
                for i in range(5):
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
            return JsonResponse({"":""},status=200)
        else:
            return JsonResponse({"":""},status=200)








########################### 3CS ####################
class CS3(APIView):
    def post(self,request):
        p = Post.objects.filter(promo="3CS")
        np=p.count()
        f = FicheDeVoeux.objects.filter(promo="3CS")
        nf=f.count()
        d = round(np/nf)
        queryFiche = FicheDeVoeux.objects.filter(promo="3CS")
        queryGroup=Group.objects.filter(promo="3CS")
        queryPost = Post.objects.filter(proomo="3CS")
        for p in queryPost:
            if p.Student:
                fiche=FicheDeVoeux()




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
            print(listLeaders[i])
            group_fiche=FicheDeVoeux.objects.get(groupfiche=choosed_group)
            for i in range(2): ##### 2 =variable of max choices
                for post in queryPost:
                    print(i)
                    if post == group_fiche.choices[i] and d > post.project_choice_count():
                            print(post.project_choice_count())
                            group_fiche.selected_project = post
                            group_fiche.save()
                            print("done!")
                            #queryFiche.exclude(groupfiche=group.groupfiche)
                            listLeaders.pop()
                            if 2 <= post.project_choice_count():
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
                for i in range(5):
                    for post in queryPost:
                        if post == group_fiche.choices[i] and d > post.project_choice_count():
                                group_fiche.selected_project = post
                                queryFiche.exclude(groupfiche=group.groupfiche)
                                listLeaders.pop()
                                if d <= post.project_choice_count():
                                    title=post.title
                                    queryPost.exclude(title=title)
                                    #queryPost.exclude(post)

                                    break
                                else:
                                    continue
                    break
                break
            return JsonResponse({"if":"if"},status=200)   
        else:
            return JsonResponse({"else":"else"},status=200  )
###########prblm if d<1





















#def test(request):
#    form=MyForm()
#    if form.is_valid:
#        print(request.POST.get("Promo"))
#        return render(request, 'projects.html', {'form': form})
#
#
#
#
#
#def Affecatation(request):
#       
#        np = Post.objects.count()  #######d<1 Probleme 
#        nf = FicheDeVoeux.objects.count() ###### filter by Promo
#        d = round(nf/np)
#       # if request.method=="POST":
#        form=MyForm()
#        if form.is_valid:
#                promo=request.POST.get("Promo")
#                print(promo)
#                #qyeryGroup=Groups.objects.get(prom)
#                queryFiche = FicheDeVoeux.objects.filter(promo=promo)
#                for q in queryFiche:
#                    print(q)
#                queryPost = Post.objects.all()
#                for group in queryFiche:
#                    #print(group)
#                    choosed_group = random.choice(queryFiche)
#                    #print(choosed_group)
#                    for i in range(2): ###max choices of every Group
#                        for post in queryPost:
#                            if post == choosed_group.choices[i] and 10 > post.project_choice_count():
#                                    choosed_group.selected_project = post
#                                    choosed_group.save()
#                                    print("Done !")
#                                    queryFiche.exclude(groupfiche=group.groupfiche)
#                                    #queryFiche.exclude(choosed_group)
#                                    if 0 <= post.project_choice_count():
#                                        title=post.title
#                                        queryPost.exclude(title=title)
#                                        #queryPost.exclude(groupfiche=group.groupfiche)
#                                        break
#                                    else:
#                                        continue
#                            else:
#                                continue
#                        
#                        break
#                        
#                    
#                if (queryFiche != None and queryPost == None):
#                    queryPost2 = Post.objects.filter(promo=promo)
#                    for group in queryFiche:
#                        choosed_group = random.choice(queryFiche)
#                        for i in range(5):
#                            for post in queryPost2:
#                                if post == choosed_group.choices[i]:
#                                        choosed_group.selected_project = post
#                                        choosed_group.save()
#                                        queryFiche.exclude(groupfiche=group.groupfiche)
#                                        title=post.title
#                                        queryPost2.exclude(title=title)
#                                        break
#                                else:
#                                        continue
#                            break
#                        break
#                    return render(request, 'projects.html', {'form': form})
#                
#                else:
#                    return render(request, 'projects.html', {'form': form})








    
        