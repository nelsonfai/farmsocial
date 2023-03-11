
from django.db import models


# Create your models here.
from django.db import models
from accounts.models import CustomUser
#from django.contrib.auth.models import CustomUser
class Network(models.Model):
    user = models.OneToOneField(CustomUser, related_name='myfollowing', on_delete=models.CASCADE)

    follower = models.ManyToManyField(CustomUser ,related_name='follows_me')
    following = models.ManyToManyField(CustomUser,related_name='i_follow')

    def __str__(self):
        return self.user.last_name
