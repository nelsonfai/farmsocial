# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django_countries.fields import CountryField
from django.core.validators import FileExtensionValidator
#from network.models import Follow

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:
        raise ValidationError(
            _("The file size must be less than 10MB.")
        )

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff',True)
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField( max_length=100 , blank=False)
    last_name= models.CharField( max_length=100 , blank=False )

    bio=models.CharField(max_length=400,blank=True, null=True)
    location = CountryField(blank_label='(select country)')
    profile_pic=models.ImageField( upload_to='profilepics/' ,blank=True, null=True,validators=[FileExtensionValidator(['jpg','png','jpeg']),  validate_file_size])
    is_student = models.BooleanField(default=False)
    course = models.CharField(max_length=100 ,blank=True, null=True)
    instituition = models.CharField(max_length=100 ,blank=True, null=True)

    profession=models.CharField(max_length=100 ,blank=True, null=True)
    company = models.CharField(max_length=100 ,blank=True, null=True)

    date_joined = models.DateTimeField( auto_now_add=True)
    is_active = models.BooleanField( default=True)
    is_verified = models.BooleanField( default=False)
    token = models.CharField(max_length=200,default=1)

    #following = models.ManyToManyField('self', through='Follow', related_name='followed_by', symmetrical=False)

    #username = models.CharField(max_length=100 ,blank=True, null=True, unique=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
   

    objects = UserManager()
    def __str__(self):
        return self.last_name
    def profilepic (self):
        if self.profile_pic:
            return self.profile_pic.url
        else:
            return 'https://myagricdiary-space.fra1.cdn.digitaloceanspaces.com/agric-static%2Fimages%2Fimages-removebg-preview.png'