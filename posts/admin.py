from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    #readonly_fields = ["user","Student","Entreprise","promo","title","introduction","tools","details","tags"]
    list_display = ('title', "user","Student","Entreprise",'promo','creating_date','approved')
    list_filter = ('promo','approved')
    
    def has_add_permission(self, request):
        return True
    def has_delete_permission(self, request, obj=None):
        return True

admin.site.register(Post,PostAdmin)
#admin.site.register(StudentPost)