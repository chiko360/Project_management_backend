from django.db import models
from django.core.mail import send_mail
from users.models import User
from pfe import settings
import uuid


class Notification(models.Model):

    nid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.SET_NULL, blank=True, null=True)
    seen = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.title

class Meta:
    ordering = ("created_on",)
    db_table = "notifications"

def sendNotification(receiver,title,body):
       
        
        
        notification = Notification()
        notification.title = title
        notification.body = body
        notification.receiver = receiver
        notification.save()
        send_mail(title,body, 'gihkhikk@gmail.com',(receiver.email,), fail_silently=False)
        return 'sent'
    
