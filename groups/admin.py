from django.contrib import admin
from .models import *
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from notifications.models import sendNotification
from pfe import settings
from django.template.response import TemplateResponse
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
from groups.form import ContactForm
from .functions import *


global var
class GroupAdmin(admin.ModelAdmin):

    change_list_template = "setGroupMembers.html"
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('set_maxgroup/', self.setGroupMembers),
        ]
        return my_urls + urls

    def setGroupMembers(self, request):
        query = request.POST['setMax']
        obj=Max.objects.get(id=1)
        obj.maxMembers=query
        obj.save()
        
        
        title = 'Group max member limit changed'
        body = 'the group max members limit changed to '+ str(query) 
        channel = 'Groups'
        event = 'MaxMembers'
        sendNotification(request.user,title,body,channel,event) 
        return HttpResponseRedirect("../")

    def full_group(self, group):
        return (group.member_count() > int(settings.MAXMEMBERS))
    
    full_group.boolean = True
    list_display = ('groupName','leader','full_group')
    #readonly_fields = ('groupName','leader')
    search_fields = ('groupName',)

    def get_ordering(self, request):
        return ['groupName']

    #def has_add_permission(self, request):
    #    return False
    #def has_delete_permission(self, request, obj=None):
    #    return False

class FicheAdmin(admin.ModelAdmin):

    change_list_template = "setChoices.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('set_max_choices/', self.setChoices),
            path('sort/', self.tirage_au_sort),
            path('results/',self.results),
            path('results/<str:promo>/',self.results),

            

        ]
        return my_urls + urls

    def results(self,request,promo):
        promo=promo
        print(promo)
        if promo=="3CS  ISI":
            promo="3CS / ISI"
        if promo=="3CS  SIW":
            promo="3CS / SIW"
        if promo=="2CS ISI":
            promo="2CS / ISI"
        if promo=="2CS SIW":
            promo="2CS / SIW"
        fiches=FicheDeVoeux.objects.filter(promo=promo)
        print(promo)
        print(fiches)
        return render(request, 'finalresults.html',{'results': fiches,'promo':promo})        

    def setChoices(self, request):
        query = request.POST['setMax']

        obj=Max.objects.get(id=1)
        obj.maxChoices=query
        obj.save()
        title = 'Max choices in fiche de voeux changed'
        body = 'the Max choices in fiche de voeux changed changed to '+ str(query) 
        channel = 'Groups'
        event = 'MaxChoices'
        sendNotification(request.user,title,body,channel,event) 
        return HttpResponseRedirect("../")
    
    def tirage_au_sort(self, request):
        #context = dict(
        #    self.admin_site.each_context(request), # Include common variables for rendering the admin template.
        #
        # )
            form = ContactForm()
            context = {'form': form}
            if request.method == "POST":
                form = ContactForm(request.POST)
                if form.is_valid():
                    methode = form.cleaned_data.get("method")
                    promo = form.cleaned_data.get("promo")
                    if methode=="random":
                        randome(promo)
                        return HttpResponseRedirect("../results/"+promo)
                    elif methode=="leader mark":
                        leader_mark(promo)
                        return HttpResponseRedirect("../results/"+promo)
                    elif methode=="group mark":
                        group_mark(promo)
                        return HttpResponseRedirect("../results/"+promo)
                    else: return HttpResponse("invalid methode")
                else: return render(request, 'sortProjects.html', 
                                        {'form': form})        
            else :
                return render(request, 'sortProjects.html', 
                                        {'form': form})

    


admin.site.register(Group,GroupAdmin)
admin.site.register(FicheDeVoeux,FicheAdmin)
admin.site.register(Max)



