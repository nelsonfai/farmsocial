from unicodedata import category
from django.db import models
from django.core.validators import FileExtensionValidator
from company.models import Company
from accounts.models import CustomUser


from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:
        raise ValidationError(
            _("The file size must be less than 10MB.")
        )

# Create your models here.
category=(
    ("none","none"),
    ("Grains","Grains"),
    ("Vegetables","Vegetables"),
    ("Fruits","Fruits"),
    ("Industrial crops","Industrial crop")
    ,("Cereals","Cereals"),
    ("livestock","livestock"),
     ("Processed","Processed"),
      ("Farm inputs","Farm inputs")
)
class ProductItem(models.Model):
    user_profile=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    companypage = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True,null=True,related_name='companyproduct')
    product=models.CharField(max_length=200 )
    product_description=models.CharField(max_length=400 )
    quantity=models.CharField(max_length=200 )
    price=models.CharField(max_length=200 )
    location=models.CharField(max_length=200)
    thumpnail=models.ImageField(upload_to='market/thumpnail')
    main_image=models.ImageField(upload_to='market/',validators=[FileExtensionValidator(['jpg','png','jpeg']),validate_file_size])
    image2=models.ImageField(blank=True, null=True ,help_text='Optional',upload_to='market/',validators=[FileExtensionValidator(['jpg','png','jpeg']),validate_file_size])
    image3=models.ImageField(blank=True, null=True,help_text='Optional', upload_to='market/',validators=[FileExtensionValidator(['jpg','png','jpeg']), validate_file_size])
    product_category=models.CharField(choices=category, max_length=20, default='none')
    view_count=models.IntegerField(default=0 )
    
    def __str__(self):
        return self.product
   
        