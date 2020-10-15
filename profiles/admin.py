from django.contrib import admin
from .models import * 

class StudentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'birth_date','gender','promo','my_group')
    list_filter = ["promo","gender","have_group"]
    #readonly_fields = ["my_group","have_group"]
    search_fields = ('last_name','first_name')

    def get_ordering(self, request):
        return ['last_name']

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'birth_date','gender','grade')
    list_filter = ["grade","gender",]
    search_fields = ('last_name','first_name')

    def get_ordering(self, request):
        return ['last_name']

admin.site.register(StudentProfile,StudentAdmin)
admin.site.register(TeacherProfile,TeacherAdmin)
admin.site.register(EntrepriseProfile)