from .models import Events
from django import forms

class EventForm(forms.ModelForm):
    
    class Meta:
        model =Events
        fields=['title','description','location','start_date','end_date']

        widgets ={
            
            'description': forms.Textarea(attrs={'class':'description','placeholder':'Event Info ...', 'rows':5,}),
            'start_date': forms.DateInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateInput(attrs={'type': 'datetime-local'})


        }        

