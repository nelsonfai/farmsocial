from django.db import models
from accounts.models import CustomUser
from django.core.validators import FileExtensionValidator
#from network.models import Follow
import uuid
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:
        raise ValidationError(
            _("The file size must be less than 10MB.")
        )

# Create your models here.
class Company(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='company_admin')
    name =models.CharField(max_length=200,blank=False,null=True)
    description =models.CharField(max_length=600)
    website = models.URLField(blank=True,null=True)
    sector = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='profilepics/company/' ,blank=True, null=True,validators=[FileExtensionValidator(['jpg','png','jpeg']),  validate_file_size])
    address = models.CharField(max_length=200)
    email = models.EmailField(blank=True,null=True)
    phonenumber = models.CharField(max_length=200,blank=True,null=True)
    founded_on = models.DateField(blank=True,null=True)
    linkedin = models.URLField(blank=True,null=True)
    instagram = models.URLField(blank=True,null=True)
    facebook = models.URLField(blank=True,null=True)
    Twitter = models.URLField(blank=True,null=True)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    pagefollowers = models.ManyToManyField(CustomUser,related_name='pagefollowers', blank=True,null=True )

    def logopic(self):
        if self.logo:
            return self.logo.url
        else:
            return 'https://myagricdiary-space.fra1.cdn.digitaloceanspaces.com/agric-static%2Fimages%2Fcompanyprofiledefault.png'