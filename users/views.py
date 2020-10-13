from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializer import UserLoginSerializer
from .serializers import ChangePasswordSerializer
from django.shortcuts import render, redirect
from .models import User
from .forms import UserLoginForm
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated   
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from notifications.models import sendNotification
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )

class UserLoginView(RetrieveAPIView):
    
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email__exact=request.data["email"])
        is_teacher = user.is_teacher
        is_student = user.is_student
        
        if is_teacher and is_student:
            account = "you cant be both student and teacher"
        elif is_teacher and not is_student:
            account = "teacher"
        elif not is_teacher and is_student:
            account = "student"
        else :
            account = "no account type specified"

        response = {
            'success' : 'True',
            'account_type': account,
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

def HomeView(request):
    return render(request,"home.html")


class ChangePwView(generics.UpdateAPIView):
        permission_classes = []
        authentication_class = JSONWebTokenAuthentication
        serializer_class = ChangePasswordSerializer
        model = User
        def get_object(self, queryset=None):
            obj = self.request.user
            return obj
        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                title = 'password changed'
                body = 'your password has been changed succesfully'
                channel = 'users'
                event = 'chgpass'
                sendNotification(self.object,title,body,channel,event)  
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)