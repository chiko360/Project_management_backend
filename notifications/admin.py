from django.contrib import admin
from .models import Notification
# Register your models here.
class NotifAdmin(admin.ModelAdmin):
    list_display = ('title','receiver','created_on')
    readonly_fields = ["title","body","created_on","receiver","seen"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_ordering(self, request):
        return ['-created_on']

admin.site.register(Notification,NotifAdmin)

