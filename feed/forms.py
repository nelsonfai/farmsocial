from .models import Comments,Articles
from django import forms
from ckeditor.fields import RichTextField
from taggit.forms import TagWidget
import io

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


    
class CommentForm(forms.ModelForm):
    
    class Meta:
        model =Comments
        fields=['comment']

        widgets ={
            
            'comment': forms.Textarea(attrs={'class':'comment_field','placeholder':'Leave a comment here...', 'rows':3,})
        }        


class ArticleForm(forms.ModelForm):
    body= RichTextField()
    postimages = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Articles
        fields = ['title','article_image','tag','postimages','video']
        widgets = {
            'tag': TagWidget(attrs={'placeholder': 'e.g: climate change,sustainablity,soil'}),
        }  

    def __init__(self,*args,**kwargs):
        super(ArticleForm,self).__init__(*args,**kwargs)

        self.fields['title'].widget.attrs['placeholder']='*** Optional'

