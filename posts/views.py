from django.shortcuts import render
from django.utils import timezone
from rest_framework.generics import( ListAPIView,
                                    RetrieveAPIView,
                                    UpdateAPIView,
                                    DestroyAPIView,
                                    CreateAPIView,)
from .models import Post
from .serializers import *
from profiles.models import  *
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.views import APIView
from django.views.generic import View
from notifications.models import sendNotification
from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
from session.permissions import DepotDeProjet,ValidationDesProjet,ChoixDesProjet,Groupment,ResultasFinal


#class PostListView3CS(APIView):
class MyPostsStudent(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    def  get(self,request):
            if request.user.is_student==True:
                owner=StudentProfile.objects.get(user=request.user)
                promo=owner.promo
                posts=Post.objects.filter(Student=owner,promo=promo)
                serializer=GetSerializer(posts,many=True)
                return JsonResponse(serializer.data,status=200,safe=False)
            else: 
                return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class createPostStudent(APIView):
    permission_classes = (IsAuthenticated,) #DepotDeProjet
    def post(self,request):
                student=StudentProfile.objects.get(user=request.user)
                promo=student.promo
                print(promo)
                if (request.user.is_student==True) and (promo=="3CS / ISI" or promo=="3CS / SIW"):
                    serializer=PostSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                            student=StudentProfile.objects.get(user=request.user)
                            title=serializer.data["title"]
                            promo=serializer.data["promo"]
                            tags=serializer.data["tags"]
                            introduction=serializer.data["introduction"]
                            tools=serializer.data["tools"]
                            details=serializer.data["details"]
                            post=Post(title=title,promo=promo,tags=tags,introduction=introduction,tools=tools,details=details,Student=student)
                            post.save()
                            #title = 'project added' 
                            #body = "your project has been submitted to the administration for revision"
                            #channel = 'projects'
                            #event = 'projectcreated'
                            #sendNotification(request.user,title,body,channel,event)
                            return JsonResponse({"note":"Post Succesfuly Created",
                                    "status":"succes"},status=status.HTTP_200_OK)
                    else:
                            return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                else: return JsonResponse({"note":"Only 3CS students can Create posts"},status=200)


class UpdatePostStudent(APIView):
    permission_classes = (IsAuthenticated,) #DepotDeProjet
    def put(self,request,pk):
            if request.user.is_student==True:
                q=Post.objects.get(id=pk)
                if q.approved==False:
                    if q.Student.user==request.user:
                        serializer=PostSerializer(q,data=request.data)
                        if serializer.is_valid():
                            serializer.save(creating_date=timezone.now())
                            serializer.save()
                            title = q.__str__()
                            body = q.__str__() +" has been updated succesfully"
                            channel = 'projects'
                            event = 'projectupdated'
                            sendNotification(request.user,title,body,channel,event)
                            return JsonResponse({"note":"Post Succesfuly UPDATED",
                                    "note":"Post Succesfuly UPDATED"},status=status.HTTP_200_OK)
                        else:
                            return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return JsonResponse({'note':'This post does not belong to you'},status=status.HTTP_404_NOT_FOUND)
                else: return JsonResponse({"note":"can't edit approved post"},status=status.HTTP_404_NOT_FOUND)
            else: return JsonResponse({"note":"teachers can't update posts"})




class DeletePostStudent(APIView):
    def delete(self,request,pk):
       
                if request.user.is_student==True:
                    q=Post.objects.get(id=pk)
                    student = StudentProfile.objects.get(user=request.user)
                    if (q.Student==student):
                        q.delete()
                        title = 'project deleted'
                        body = "your project has been deleted succesfully"
                        channel = 'projects'
                        event = 'projectdeletedted'
                        sendNotification(request.user,title,body,channel,event)
                        return JsonResponse({'success': 'True',
                                'Note':'Post succesfully deleted !'}, status = status.HTTP_200_OK)
                    else: return JsonResponse({'note':'This post does not belong to you'},status=status.HTTP_404_NOT_FOUND)
                else: return JsonResponse({"note":"teachers can't Delete posts"})
       


@api_view(["PUT"])
def PostUpdate(request,pk):
    permission_classes = (IsAuthenticated,) #DepotDeProjet
    authentication_class = JSONWebTokenAuthentication
    if request.method=="PUT": 
        if request.user.is_teacher==True:
            q=Post.objects.get(id=pk)
            if q.approved==False:
                if q.user.user==request.user:
                    serializer=PostSerializer(q,data=request.data)
                    if serializer.is_valid():
                        serializer.save(creating_date=timezone.now())
                        serializer.save()
                        title = q.__str__()
                        body = q.__str__() +" has been updated succesfully"
                        channel = 'projects'
                        event = 'projectupdated'
                        sendNotification(request.user,title,body,channel,event)
                        return JsonResponse({"note":"Post Succesfuly UPDATED",
                                "note":"Post Succesfuly UPDATED"},status=status.HTTP_200_OK)
                    else:
                        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                else:
                    return JsonResponse({'note':'This post does not belong to you'},status=status.HTTP_404_NOT_FOUND)
            else: return JsonResponse({"note":"can't edit approved post"},status=status.HTTP_404_NOT_FOUND)
        else: return JsonResponse({"note":"Students can't update posts"})
    else: return  JsonResponse({"note":"Only PUT method allowed"})
           
@api_view(['DELETE'])
def PostDelete(request,pk):
    permission_classes = (IsAuthenticated,) #DepotDeProjet
    authentication_class = JSONWebTokenAuthentication
    if request.method =="DELETE":
            if request.user.is_teacher==True:
                q=Post.objects.get(id=pk)
                teacher = TeacherProfile.objects.get(user=request.user)
                if (q.user==teacher):
                    q.delete()
                    title = 'project deleted'
                    body = "your project has been deleted succesfully"
                    channel = 'projects'
                    event = 'projectdeletedted'
                    sendNotification(request.user,title,body,channel,event)
                    return JsonResponse({'success': 'True',
                            'Note':'Post succesfully deleted !'}, status = status.HTTP_200_OK)
                else: return JsonResponse({'note':'This post does not belong to you'},status=status.HTTP_404_NOT_FOUND)
            else: return JsonResponse({"note":"Students can't Delete posts"})
    else: 
            return JsonResponse({"method":"not allowed"},status=status.HTTP_406_NOT_ACCEPTABLE)

class PostListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    def  get(self,request):
        student=StudentProfile.objects.get(user=request.user)
        print(student)
        promo=student.promo
        print(promo)
        posts=Post.objects.filter(promo=promo,approved=True)
        print(posts)
        serializer=GetSerializer(posts, many=True)
        return JsonResponse(serializer.data,status=200,safe=False)

class PostToEditView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    def  get(self,request,id):
        if request.user.is_teacher==True:
            owner=TeacherProfile.objects.get(user=request.user)
            posts=Post.objects.get(user=owner,id=id)
            serializer=PostSerializer(posts)
            return JsonResponse(serializer.data,status=200,safe=False)

class TeacherPostView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    def  get(self,request):
            if request.user.is_teacher==True:
                owner=TeacherProfile.objects.get(user=request.user)
                posts=Post.objects.filter(user=owner)
                serializer=GetSerializer(posts,many=True)
                return JsonResponse(serializer.data,status=200,safe=False)
            else: 
                return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PostDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    queryset=Post.objects.all()
    serializer_class=GetSerializer
    lookup_field= "title"

@api_view(['POST'])
def create(request):
    permission_classes = (IsAuthenticated,) #DepotDeProjet
    authentication_class = JSONWebTokenAuthentication
    if request.method =="POST":
        if request.user.is_teacher==True:
            serializer=PostSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                    teacher=TeacherProfile.objects.get(user=request.user)
                    title=serializer.data["title"]
                    promo=serializer.data["promo"]
                    tags=serializer.data["tags"]
                    introduction=serializer.data["introduction"]
                    tools=serializer.data["tools"]
                    details=serializer.data["details"]
                    post=Post(title=title,promo=promo,tags=tags,introduction=introduction,tools=tools,details=details,user=teacher)
                    post.save()
                    title = 'project added' 
                    body = "your project has been submitted to the administration for revision"
                    channel = 'projects'
                    event = 'projectcreated'
                    sendNotification(request.user,title,body,channel,event)
                    return JsonResponse({"note":"Post Succesfuly Created",
                            "status":"succes"},status=status.HTTP_200_OK)
            else:
                    return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else: return JsonResponse({"note":"Students can't Create posts"})
    else: return  JsonResponse({"note":"Only POST method allowed"})

      
  


        




