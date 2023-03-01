from django.db import models
# Create your models here.
from account.models import CustomUser
from ckeditor.fields import RichTextField
from account.models import CustomUser
from django.utils import timezone
from taggit.managers import TaggableManager
from django.core.validators import FileExtensionValidator
from company.models import Company
import math
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:
        raise ValidationError(
            _("The file size must be less than 10MB.")
        )

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


class Articles (models.Model):
    author=models.ForeignKey(CustomUser, related_name='profile' ,on_delete= models.CASCADE ,blank=True, null=True)
    company = models.ForeignKey(Company,related_name='companyprofile' ,on_delete= models.CASCADE, blank=True, null=True)
    title = models.CharField( max_length=400, blank=True, null=True)
    #body = models.TextField()
    body = RichTextField( blank=True, null=True ,db_index=True)
    slug = models.SlugField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    article_image = models.ImageField(upload_to='articlepics/', blank=True, null=True,validators=[FileExtensionValidator(['jpg','png',]),validate_file_size])
    thumpnail = models.ImageField( upload_to='articlepics/thumbnails/',blank=True, null=True ,default='/images/articleholder.jpg' )
    likes =models.ManyToManyField(CustomUser, default=None,blank=True, related_name='liked')
    #tagline=models.CharField(max_length=100 ,blank=True,null=True)
    tag = TaggableManager(blank=True)

  
   
    def __str__(self):
        if self.title:
            return self.title 
        else:
            return self.body[5:15] + "..."
            
    def snippet(self):
        return self.body[:240] + "..."  

    def whenpublished(self):
        return timefuntion(self.date)
       
    
    @property
    def num_likes(self):
        return self.liked.all().count()

class Comments (models.Model):
    
    article= models.ForeignKey(Articles, related_name='comments' ,on_delete= models.CASCADE)
    comment= models.TextField()
    date= models.DateTimeField(auto_now=True)
    author=models.ForeignKey(CustomUser,on_delete= models.CASCADE,blank=True,null=True) 
    companyauthor=models.ForeignKey(Company,on_delete= models.CASCADE,blank=True,null=True) 

    

    def __str__(self):
        return f'{self.author.id} commented on {self.article.title}' 
    
LIKE_CHOICES=(
    ('Like','Like'), ('Unlike','Unlike'))

class Like(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    company=models.ForeignKey(Company,on_delete= models.CASCADE,blank=True,null=True) 
    article=models.ForeignKey(Articles,on_delete=models.CASCADE)
    value =models.CharField(choices =LIKE_CHOICES, default='Like', max_length=10)

announce_type=(
    ('I have','I have'), ('I need','I need'),
    ('Select','Select'))

class Announcements(models.Model):
    profile=models.ForeignKey(CustomUser, related_name='annouce_profile' ,on_delete= models.CASCADE, default=None)
    annoucement= models.CharField(max_length=100 ,blank=True, null=True)
    annoucement_type= models.CharField(choices =announce_type, default='Select', max_length=10)
    date= models.DateTimeField(auto_now=True)

  
    def whenpublished(self):
        return timefuntion(self)

