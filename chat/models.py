
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
#from django.contrib.auth.models import User
from accounts.models import CustomUser

# Create your models here


class ThreadManager(models.Manager):
    
    def by_user(self, **kwargs):
        #user = kwargs.get('user')
        user=kwargs.get('user')
        lookup = Q(first_person= user ) | Q( second_person = user) 
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
 
    timestamp = models.DateTimeField(auto_now_add=True)

    
    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']

class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
