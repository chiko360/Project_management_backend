import datetime

from rest_framework import permissions
from .models import Session

class DepotDeProjet(permissions.BasePermission):
    message="la phase de depot de projet et expire"
    def has_permission(self,request,view):
        CurrentDate = datetime.datetime.now()
        try:
            depotDeProjet=Session.objects.get(name="Depot De Projet")
        except Session.DoesNotExist:
            depotDeProjet=None
        
        if (CurrentDate>depotDeProjet.starting_date and CurrentDate<depotDeProjet.ending_date):
            return True
        else:
            return False

            

class ValidationDesProjet(permissions.BasePermission):
    message="la phase de Validation Des Projet de projet et expire"
    def has_permission(self,request,view):
        CurrentDate = datetime.datetime.now()
        try:
            phase=Session.objects.get(name="Validation des projet")
        except Session.DoesNotExist:
            phase=None
        
        if (CurrentDate>phase.starting_date and CurrentDate<phase.ending_date):
            return True
        else:
            return False 




class ChoixDesProjet(permissions.BasePermission):
    message="la phase de Choix des projet et expire"
    def has_permission(self,request,view):
        CurrentDate = datetime.date.today()
        try:
            phase=Session.objects.get(name="Choix de projet")
        except Session.DoesNotExist:
            phase=None
        
        if (CurrentDate>phase.starting_date and CurrentDate<phase.ending_date):
            return True
        else:
            return False 




class Groupment(permissions.BasePermission):
    message="la phase de Groupment et expire"
    def has_permission(self,request,view):
        CurrentDate = datetime.date.today()
        try:
            phase=Session.objects.get(name="Groupment")
        except Session.DoesNotExist:
            phase=None
        
        if (CurrentDate>phase.starting_date and CurrentDate<phase.ending_date):
            return True
        else:
            return False 





class ResultasFinal(permissions.BasePermission):
    message="la phase de Resultas Final et expire"
    def has_permission(self,request,view):
        CurrentDate = datetime.datetime.now()
        try:
            phase=Session.objects.get(name="Resultas final")
        except Session.DoesNotExist:
            phase=None
        
        if (CurrentDate>phase.starting_date and CurrentDate<phase.ending_date):
            return True
        else:
            return False 

