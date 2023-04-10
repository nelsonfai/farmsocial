
from django.db import models
from accounts.models import CustomUser
import math
from django.utils import timezone
from django.db.models import Exists, OuterRef
from django.db.models import Sum


def timefuntion(date):
        now = timezone.now()
        
        diff= now - date

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"


class Forum(models.Model):
    topic = models.CharField(max_length=100)
    room_description= models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(CustomUser, related_name='forums_joined')
    is_public = models.BooleanField(default=False)
    identifier =models.CharField(max_length=200, unique=True,blank=False,null=False)

    def __str__(self):
        return self.topic
    def whenpublished(self):
        return timefuntion(self.created_at)
    
    @property
    def total_upvotes(self):
        count = self.forum_messages.aggregate(Sum('upvote'))['upvote__sum']
        if count:
            return count
        else:
            return 0

class Message(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='forum_messages')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    upvote = models.IntegerField(default=0)
    read_by=models.ManyToManyField(CustomUser, related_name='read_by')

    def __str__(self):
        return f"{self.author} ({self.timestamp}): {self.content}"
    def whenpublished(self):
        return timefuntion(self.timestamp)