from django.db import models

# Create your models here.
class Session(models.Model):

    starting_date=models.DateField()
    ending_date=models.DateField()
    name=models.CharField(max_length=200,null=False)

    def __str__(self):
        return (self.name)
    
