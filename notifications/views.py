from django.shortcuts import render
from pfe import settings
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
import pusher

class PusherAuthView(APIView):
    authentication_classes = JSONWebTokenAuthentication
    permission_classes = [IsAuthenticated]

    pusher_client = pusher.Pusher(
        app_id= settings.PUSHER_APP_ID,
        key= settings.PUSHER_KEY,
        secret= settings.PUSHER_SECRET,
        cluster= settings.PUSHER_CLUSTER,
            )

    def post(self, request):
        channel_name = self.request.data['channel_name']
        socket_id = self.request.data['socket_id']

        auth = self.pusher_client.authenticate(
            channel = channel_name,
            socket_id = socket_id
            )
        
        return Response(auth)

class UnseenNotifications(APIView):
    def get(self, request):
        authentication_classes = JSONWebTokenAuthentication
        permission_classes = [IsAuthenticated]
        notifications=Notification.objects.filter(receiver=request.user,seen=False)
        serializer=NotificationSerializer(notifications, many=True)
        return JsonResponse(serializer.data,status=200,safe=False)