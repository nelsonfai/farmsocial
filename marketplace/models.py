from unicodedata import category
from django.db import models

from account.models import CustomUser
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
    product=models.CharField(max_length=200 )
    product_description=models.CharField(max_length=400 )
    quantity=models.CharField(max_length=200 )
    price=models.CharField(max_length=200 )
    location=models.CharField(max_length=200)
    main_image=models.ImageField(upload_to='market/',)
    image2=models.ImageField(blank=True, null=True ,help_text='Optional',upload_to='market/',)
    image3=models.ImageField(blank=True, null=True,help_text='Optional', upload_to='market/')
    product_category=models.CharField(choices=category, max_length=20, default='none')
    view_count=models.IntegerField(default=0 )
    
    def __str__(self):
        return self.product
