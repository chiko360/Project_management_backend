from django.shortcuts import render
from pfe import settings
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer



class UnseenNotifications(APIView):
    def get(self, request):
        authentication_classes = JSONWebTokenAuthentication
        permission_classes = [IsAuthenticated]
        notifications=Notification.objects.filter(receiver=request.user,seen=False)
        serializer=NotificationSerializer(notifications, many=True)
        return JsonResponse(serializer.data,status=200,safe=False)