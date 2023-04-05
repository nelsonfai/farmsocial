from django.db import models
from django.db.models import  Manager
from company.models import Company
from accounts.models import CustomUser

class Events(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='event_users',null=True,blank=True)
    page =models.ForeignKey(Company,on_delete=models.CASCADE,related_name='event_page',null=True,blank=True)
    title =models.CharField(max_length=400)
    description=models.CharField(max_length=600)
    location =models.CharField(max_length=400)
    start_date =models.DateTimeField()
    end_date =models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    attending = models.ManyToManyField(CustomUser,related_name='attendees')
    expired =models.BooleanField(default=False)
    slug= models.SlugField()

    def __str__(self):
        return self.title