import uuid
from django.db import models
from users.models import *
from groups.models import Group

class StudentProfile(models.Model):
    genders = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    Niveaux = [
        ('2CP', '2eme année'),
        ('1CS', '3eme année'),
        ('2CS ISI ', '4eme année ISI'),
        ('2CS SIW ', '4eme année SIW'),
        ('3CS / ISI', '5eme année ISI'),
        ('3CS / SIW', '5eme année SIW'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User,limit_choices_to={'is_student': u'True'}, on_delete=models.CASCADE, related_name='student_profile')
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    birth_date= models.DateField(blank=False,null=False)
    gender = models.CharField(max_length=1, choices=genders,null=False,blank=False)
    promo = models.CharField(max_length=9,choices=Niveaux,null=False,blank=False)
    marks = models.PositiveIntegerField(default=0, null=True) 
    picture = models.ImageField(upload_to='uploads/images/students',blank=True, null=True)
    my_group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name="members",null=True,blank=True,)
    have_group=models.BooleanField(default=False)
    
    def invites(self):
        return self.invited_member.all()

    def __str__(self):
        return str(self.last_name +" "+ self.first_name)
    
    class Meta:
        verbose_name_plural = "Students"
        '''
        to set table name in database
        '''
        db_table = "student_profile"

class TeacherProfile(models.Model):
    genders = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    grades = [
        ('Pro','Professeur'),
        ('MAA','Maitre-assistant A'),
        ('MAB','Maitre-assistant B'),
        ('MCA','maitre conférence A'),
        ('MCB','maitre conférence B'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, limit_choices_to={'is_teacher': u'True'},on_delete=models.CASCADE, related_name='teacher_profile')
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    birth_date= models.DateField(blank=False,null=False)
    gender = models.CharField(max_length=1, choices=genders,null=False,blank=False)
    grade = models.CharField(max_length=3,choices=grades,null=False,blank=False)
    picture = models.ImageField(upload_to='uploads/images/teacher', blank=True, null=True)
    
    def __str__(self):
        return (self.last_name +" "+ self.first_name)
    
    class Meta:
        verbose_name_plural = "Teachers"
        '''
        to set table name in database
        '''
        db_table = "teacher_profile"

class EntrepriseProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='entreprise')
    name = models.CharField(max_length=50, unique=False)
    picture = models.ImageField(upload_to='uploads/images/students',blank=True, null=True)
    
    def invites(self):
        return self.invited_member.all()

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Entreprise"
        '''
        to set table name in database
        '''
        db_table = "entreprise_table"