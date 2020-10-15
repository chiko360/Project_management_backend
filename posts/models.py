from django.db import models
from taggit.managers import TaggableManager
from profiles.models import *
from notifications.models import sendNotification
import uuid

class Post(models.Model):
    
    Niveaux = [
        ('2CP', '2eme année'),
        ('1CS', '3eme année'),
        ('2CS / SIW', '4eme année'),
        ('2CS / ISI', '4eme année'),
        ('3CS / SIW', '5eme année SIW'),
        ('3CS / ISI', '5eme année ISI'),
    ]
    title=models.CharField(max_length=200, unique=False)
    user = models.ForeignKey("profiles.TeacherProfile", on_delete=models.CASCADE, related_name='poster',db_constraint=False,blank=True,null=True)
    Student = models.ForeignKey("profiles.StudentProfile", on_delete=models.CASCADE, related_name='poster_studen',blank=True,null=True)
    Entreprise = models.ForeignKey("profiles.EntrepriseProfile", on_delete=models.CASCADE, related_name='poster_entreprise',blank=True,null=True)
    promo = models.CharField(max_length=9,choices=Niveaux,null=False,blank=False)
    tags = models.CharField(max_length=256)
    introduction=models.TextField()
    tools=models.TextField()
    details=models.TextField()
    creating_date= models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def save(self):
        if self.pk is not None:
            orig = Post.objects.get(pk=self.pk)
            if (orig.approved== False) and (self.approved==True) :
                title = 'project approuved' 
                body = "your project "+self.title +" has been approuved by the administration"
                if self.user != None :
                    sendNotification(self.user.user,title,body)
                elif self.Student != None :
                    sendNotification(self.Student.user,title,body)

                else :return;
                
        super(Post, self).save()

    def post_owner(self):
        return str(self.user.__str__())

    def project_choice_count(self):
        return self.selected.count()

    def project_choice_all(self):
        return self.selected.all()
        
    def __str__(self):
        return (self.title)
    
    def project_repitition(self):
        return self.choosed_projects.count()
    
    
    class Meta:
        verbose_name_plural = "Projects"
        '''
        to set table name in database
        '''
        db_table = "Projects"
