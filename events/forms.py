from .models import Events
from django import forms

class EventForm(forms.ModelForm):
    
    class Meta:
        model =Events
        fields=['title','location','start_date','end_date']

        widgets ={
            
            'start_date': forms.DateInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateInput(attrs={'type': 'datetime-local'})


        }        

