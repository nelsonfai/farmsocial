from .models import Comments,Articles
from django import forms
from ckeditor.fields import RichTextField


    
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
        widgets ={
            
            'tag': forms.TextInput(attrs={'class':'comment_field','placeholder':'e.g : climate change,soil', 'row':3,})
        }        

