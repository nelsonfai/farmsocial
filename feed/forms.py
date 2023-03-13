from .models import Comments,Articles
from django import forms
from ckeditor.fields import RichTextField
from taggit.forms import TagWidget



    
class CommentForm(forms.ModelForm):
    
    class Meta:
        model =Comments
        fields=['comment']

        widgets ={
            
            'comment': forms.Textarea(attrs={'class':'comment_field','placeholder':'Leave a comment here...', 'rows':3,})
        }        


class ArticleForm(forms.ModelForm):
    body= RichTextField()
    class Meta:
        model = Articles
        fields = ['title','article_image','tag']
        widgets = {
            'tag': TagWidget(attrs={'placeholder': 'e.g: climate change,sustainablity,soil'}),
        }  

    def __init__(self,*args,**kwargs):
        super(ArticleForm,self).__init__(*args,**kwargs)

        self.fields['title'].widget.attrs['placeholder']='*** Optional'
