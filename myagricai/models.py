from django.db import models
from django.db.models import  Manager


# Create your models here.
from accounts.models import CustomUser

class UserQA(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    question=models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    date= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.question
    objects = Manager()   # The default Manager.


