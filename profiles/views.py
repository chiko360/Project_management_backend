from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import *
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render
import pusher
from django.views.generic import TemplateView
from .serializer import HaveGroup


class StudentProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': student_profile.first_name,
                    'last_name': student_profile.last_name,
                    'birth_date': student_profile.birth_date,
                    'gender': student_profile.gender,
                    'promo': student_profile.promo,
                    }]
                }

        except Exception as e:
            status_code = 404
            response = {
                'success': 'false',
                'status code': status_code,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)


class TeacherProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            teacher_profile = TeacherProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': teacher_profile.first_name,
                    'last_name': teacher_profile.last_name,
                    'birth_date': teacher_profile.birth_date,
                    'gender': teacher_profile.gender,
                    'grade': teacher_profile.grade,
                    }]
                }

        except Exception as e:
            status_code = 404
            response = {
                'success': 'false',
                'status code': status_code,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)


class getGroup(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    def get(self,request):
        student= StudentProfile.objects.get(user=request.user)
        serializer=HaveGroup(student)
        return JsonResponse(serializer.data,status=200)