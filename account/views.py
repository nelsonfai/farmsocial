import os
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib import messages
from .forms import LogInForm,EmailForm,PersonalInfoForm,ProfileInfo,EducationForm
from formtools.wizard.views import SessionWizardView
from .models import CustomUser

from feed.models import Articles
from marketplace.models import ProductItem
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import signals
from django.dispatch import receiver
from .models import CustomUser
from notification.models import NotificationUser
from Friends.models import Network
from django.core.files.storage import FileSystemStorage






# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form =LogInForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            if 'next' in request.POST:
                messages.success(request, ("You were succesfully logged in"))
                return redirect(request.POST.get('next'))
            else:
                messages.success(request, ("You were succesfully logged in"))
                return redirect('articles')
            
    else:
        form=LogInForm()

    context={
                'form':form,

    }

    return render(request ,'account/login.html',context)


def logout_view(request):
    
        logout(request)
        messages.success(request, ("You were succesfully logged out"))
        return redirect('articles')
    
@login_required()     
def profile(request,slug):
    
    profile=CustomUser.objects.get(id = slug )
    products=ProductItem.objects.filter(user_profile=profile)
    articles=Articles.objects.filter(author=profile)
    followers = Network.objects.get(user=profile)

    context={
                'profile':profile,
                'products':products,
                'articles':articles,
                'network':followers
            }
     
    return render(request ,'account/profile.html',context)
@login_required   
def edit_profile(request):
        user = request.user
        form = PersonalInfoForm(instance=user)
        profile=form
        context={
                    'profile':profile,
                }

 
        return render (request,'account/editprofile.html',context)
@login_required(messages.error(request,'You must log in to view this page!'))     
           
def edit_name(request):
        if request.method == 'POST':
            form=PersonalInfoForm(request.POST or None,instance =request.user)
            if form.is_valid():
                user = request.user
                user.first_name=form.cleaned_data['first_name']
                user.last_name=form.cleaned_data['last_name']
                print(user.profile)
                user.save()
                return redirect('profile',request.user.id)
            else:
                user = request.user
                form = PersonalInfoForm(instance=user)
                return render (request,'account/editprofile.html',{'form':form})
        else:
            user = request.user
            form = PersonalInfoForm(instance=user)
            profile=form
            context={
                        'profile':profile,
                    }
            return render (request,'account/editprofile.html',context)

@login_required(messages.error(request, ('You must log in to view this page!'))     
       
def edit_bio(request):
        if request.method == 'POST':
            form=ProfileInfo(request.POST or None ,request.FILES,instance=request.user)
            filess= ProfileInfo(request.FILES)
            if form.is_valid():
                user = request.user
                user.bio=form.cleaned_data['bio']
                user.location=form.cleaned_data['location']
                user.profile_pic=form.cleaned_data['profile_pic']

                user.save()
                return redirect('profile',request.user.id)
            else:
                user = request.user
                form = ProfileInfo(instance=user)
                return render (request,'account/editprofile.html',{'form':form})
        else:
            user = request.user
            form = ProfileInfo(instance=user)
            profile=form
            context={
                        'profile':profile,
                    }
            return render (request,'account/editprofile.html',context)

@login_required(messages.error(request,'You must log in to view this page!'))     
       
def edit_education(request):

        if request.method == 'POST':
            form=EducationForm(request.POST or None ,instance=request.user)
            if form.is_valid:
                user= request.user
                print(form['course'].value())
                user.course=form['course'].value()
                user.is_student=form['is_student'].value()
                user.instituition=form['instituition'].value()
                user.profession=form['profession'].value()
                user.company=form['company'].value()
                user.save()
                return redirect('profile',request.user.id)
            else:
                user = request.user
                form = EducationForm(instance=user)
                return render (request,'account/editprofile.html',{'form':form})
        else:
            user = request.user
            form = EducationForm(instance=user)
            profile=form
            context={
                        'profile':profile,
                    }
            return render (request,'account/editprofile.html',context)

    

#signup user 
class SignupWizard(SessionWizardView):
    form_list = [EmailForm, PersonalInfoForm]
    template_name = 'account/emailform.html'

    def done(self, form_list, **kwargs):
        print(form_list[0]['password1'].value())
        user = CustomUser.objects.create_user(
        email=form_list[0].cleaned_data['email'],
        password=form_list[0].cleaned_data['password1'],
       first_name=form_list[1].cleaned_data['first_name'],
       last_name=form_list[1].cleaned_data['last_name'])
        user.save()

        #create user Notification 
        usernotification = NotificationUser.objects.create(user=user)
        # create user Network
        usernetwork = Network.objects.create(user=user)
        login(self.request ,user)
        return redirect('firstProfile')

class FirstProfile(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))

    form_list = [ProfileInfo,EducationForm]
    template_name = 'account/emailform.html'
    
    def done(self, form_list, **kwargs):
        user = self.request.user
        print(form_list)
        user.bio=form_list[0].cleaned_data['bio']
        user.location=form_list[0].cleaned_data['location']
        user.profile_pic=form_list[0].cleaned_data['profile_pic']
        user.is_student=form_list[1].cleaned_data['is_student']
        user.course=form_list[1].cleaned_data['course']
        user.instituition=form_list[1].cleaned_data['instituition']
        user.profession =form_list[1].cleaned_data['profession']
        user.company=form_list[1].cleaned_data['company']
        print(user.profile_pic)
        user.save()
        print('updated')
        return redirect('articles')

