from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _



class LogInForm(forms.Form):
    email_or_phone = forms.CharField( max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Mobile Number or Email address'}))
    password = forms.CharField( widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        email_or_phone = self.cleaned_data.get('email_or_phone')
        password = self.cleaned_data.get('password')
         # authenticate user
        user = authenticate(email_or_phone=email_or_phone, password=password)
        if not user:
            raise forms.ValidationError('Invalid login credentials.Keep in my password is case sensitive')
        self.user = user
        return self.cleaned_data

class EmailForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('email','phonenumber')
 
    def __init__(self,*args,**kwargs):
        super(EmailForm,self).__init__(*args,**kwargs)
        del self.fields['password2']
        del self.fields['password1']

    def cleaned_data(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phonenumber = cleaned_data.get("phonenumber")

        if CustomUser.objects.filter(phonenumber=phonenumber).exists():
            raise forms.ValidationError("Phone number already in use.")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")

class PasswordForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('password1',)
 
    def __init__(self,*args,**kwargs):
        super(PasswordForm,self).__init__(*args,**kwargs)
        del self.fields['password2']
        self.fields['password1'].help_text = None

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

class ProfilePic(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('profile_pic',)
    def __init__(self,*args,**kwargs):
        super(ProfilePic,self).__init__(*args,**kwargs)
        del self.fields['password2']
        del self.fields['password1']

class EducationForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('is_student','course','instituition','profession','company')
        labels = {'is_student': 'I am a student',
                  }

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


class PassReset(forms.Form):
    email = forms.EmailField(label='Email address', required=False)
    phonenumber = PhoneNumberField()
    fields=('email','phonenumber')
    def __init__(self,*args,**kwargs):
        super(PassReset,self).__init__(*args,**kwargs)



class ChangeEmailForm(forms.ModelForm):
    #phone_number = forms.CharField(label=_('Phone number'))
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        strip=False,
    )
    class Meta:
        model = CustomUser
        fields = ('email','phonenumber')
        labels = {
            'email': _('New email'),
            'phonenumber':_('New phone Number')
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['email'].label =f'Current Email :{self.user.email}'
        self.fields['phonenumber'].label =f'Current Phone number: {self.user.phonenumber}'
        self.fields['email'].widget.attrs['placeholder']='Enter New Email '
        self.fields['phonenumber'].widget.attrs['placeholder']='Enter New Phone number '





      
     