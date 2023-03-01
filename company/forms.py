from django.forms import ModelForm

from django import forms
from company.models import Company

class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model=Company
        fields=('name','description','sector','founded_on')
        widgets = {
            'founded_on': forms.DateInput(attrs={'type': 'date'})
        }
        def __init__(self,*args,**kwargs):
            super(CompanyCreationForm,self).__init__(*args,**kwargs)
            self.fields['name'].widget.attrs['class']='form_control'
            self.fields['description'].widget.attrs['class']='form_control'
            self.fields['sector'].widget.attrs['class']='form_control'
            self.fields['founded_on'].widget.attrs['class']='form_control'
 

class DashboardForm(forms.ModelForm):
    class Meta:
        model = Company
        __all__ = True
        exclude=('user','pagefollowers','currently')
        widgets = {
            'founded_on': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'placeholder':'Write a short self-description to introduce yourself to the community...', 'rows':6,})

        }



