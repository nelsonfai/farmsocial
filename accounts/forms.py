from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from accounts.models import CustomUser
from django.contrib.auth import get_user_model



class LogInForm(forms.ModelForm):
    email_or_phone = forms.CharField(label='Email or phone number', max_length=255)

    class Meta:
        model=CustomUser
        #password = forms.CharField(label='Password', widget=forms.PasswordInput)

        fields=('password','email_or_phone' )

    def __init__(self,*args,**kwargs):
        super(LogInForm,self).__init__(*args,**kwargs)
        #self.fields['username'].widget.attrs['class']='form_control'
        #self.fields['username'].widget.attrs['placeholder']='e.g mail@myagricdiary.com'
        self.fields['password'].widget.attrs['class']='form_control'
        self.fields['password'].widget.attrs['placeholder']='**********'

class EmailForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('email',)
 
    def __init__(self,*args,**kwargs):
        super(EmailForm,self).__init__(*args,**kwargs)
        del self.fields['password2']

class NumberForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('phonenumber',)
 
    def __init__(self,*args,**kwargs):
        super(EmailForm,self).__init__(*args,**kwargs)
        del self.fields['password2']
class PasswordForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('password1',)
 
    def __init__(self,*args,**kwargs):
        super(EmailForm,self).__init__(*args,**kwargs)
        del self.fields['password2']
        self.fields['password1'].help_text = None




    def cleaned_data(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")


class PersonalInfoForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('first_name','last_name')
    def __init__(self,*args,**kwargs):
        super(PersonalInfoForm,self).__init__(*args,**kwargs)
        del self.fields['password2']
        del self.fields['password1']
        self.fields['first_name'].widget.attrs['class']='form_control'
        self.fields['last_name'].widget.attrs['class']='form_control'
      
class PersonalInfoFormOne(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('first_name','last_name')
        last_name = forms.CharField(
        help_text='<p style="text-align:center;color:grey;font-size:small"> By clicking Send, you agree to My AgricDiary´s <a href="https://myagricdiary.com/useragreement">User Agreement,</a> <a href="https://myagricdiary.com/privacy">Privacy Policy </a> and <a href="https://myagricdiary.com/cookiepolicy">Cookie Policy </a></p>'
        )
    def __init__(self,*args,**kwargs):
        super(PersonalInfoFormOne,self).__init__(*args,**kwargs)
        del self.fields['password2']
        del self.fields['password1']
        self.fields['first_name'].widget.attrs['class']='form_control'
        self.fields['last_name'].widget.attrs['class']='form_control'

      


class ProfileInfo(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('bio','location','profile_pic')
        labels = {'bio': 'About me'}

        widgets ={
            
            'bio': forms.Textarea(attrs={'class':'form_contol','placeholder':'Write a short self-description to introduce yourself to the community...', 'rows':6,})
        }   
    def __init__(self,*args,**kwargs):
        super(ProfileInfo,self).__init__(*args,**kwargs)
        del self.fields['password2']
        del self.fields['password1']
        self.fields['bio'].widget.attrs['class']='form_control'
        self.fields['location'].widget.attrs['class']='form_control'
        self.fields['bio'].widget.attrs['placeholder']='Write a short self-description to introduce yourself to the community... '



class EducationForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('is_student','course','instituition','profession','company')
        labels = {'is_student': 'I am a student'}

    def __init__(self,*args,**kwargs):
            super(EducationForm,self).__init__(*args,**kwargs)
            del self.fields['password1']
            del self.fields['password2']
            self.fields['is_student'].widget.attrs['class']='form_control'
            self.fields['is_student'].widget.attrs['id']='checked'
            self.fields['course'].widget.attrs['class']='form_control studentinput'
            self.fields['instituition'].widget.attrs['class']='form_control studentinput'
            self.fields['profession'].widget.attrs['class']='form_control profinput'
            self.fields['company'].widget.attrs['class']='form_control profinput'

  
