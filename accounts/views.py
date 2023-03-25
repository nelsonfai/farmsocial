import os
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import LogInForm,EmailForm,PersonalInfoForm,ProfileInfo,EducationForm,PersonalInfoFormOne,PasswordForm,PassReset,ChangeEmailForm
from formtools.wizard.views import SessionWizardView
from .models import CustomUser
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django import forms
from django.utils.encoding import force_bytes, force_text

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
from django.db.models import Q
from django.http import HttpResponse
import uuid
from PIL import Image
from company.models import Company
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.template.loader import render_to_string
from mailjet_rest import Client as MailClient
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page
from django.utils.text import slugify

import io
from twilio.rest import Client

# Create your views here.
def login_view(request):
    try:
        if request.method == 'POST':
            form =LogInForm(request.POST)
            if form.is_valid():
                    login(request, form.user)
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
        return render(request ,'accounts/login.html',context)


    except:
        form=LogInForm()
        context={
        'form':form,
        }
        messages.error(request,('Oops Something went wrong.Please try again later.'))
        return render(request ,'accounts/login.html',context)

def logout_view(request):
        try:
            logout(request)
            messages.success(request, ("You were succesfully logged out"))
            return redirect('articles')
        except:
            messages.error(request,('Oops Something went wrong.Please try again later.'))
            return redirect('articles')

@cache_page(60 * 5) # cache for 5 minutes        
@login_required()     
def profile(request,slug):
    try:    
        profile=CustomUser.objects.get(ui = slug )
        products=ProductItem.objects.filter(user_profile=profile)
        articles=Articles.objects.filter(author=profile)
        followers = Network.objects.get(user=profile)

        context={
                    'profile':profile,
                    'products':products,
                    'articles':articles,
                    'network':followers
                }
        return render(request ,'accounts/profile.html',context)

    except:
            messages.error(request,('Oops Something went wrong.Please try again later.'))
            return render(request ,'accounts/profile.html',context)
    
@login_required   
def edit_profile(request):
        user = request.user
        form = PersonalInfoForm(instance=user)
        profile=form
        context={
                    'form':profile,
                }

 
        return render (request,'accounts/editprofile.html',context)
@login_required           
def edit_name(request):
    
        if request.method == 'POST':
            form=PersonalInfoForm(request.POST or None,instance =request.user)
            if form.is_valid():
                user = request.user
                user.first_name=form.cleaned_data['first_name']
                user.last_name=form.cleaned_data['last_name']
                print(user.profile)
                user.save()
                return redirect('profile',request.user.ui)
            else:
                user = request.user
                form = PersonalInfoForm(instance=user)
                return render (request,'accounts/editprofile.html',{'form':form})
        else:
            user = request.user
            form = PersonalInfoForm(instance=user)
            profile=form
            context={
                        'form':profile,
                    }
            return render (request,'accounts/editprofile.html',context)

@login_required       
def edit_bio(request):
        if request.method == 'POST':
            form=ProfileInfo(request.POST or None ,request.FILES,instance=request.user)
            photo= request.FILES.get('profile_pic')
            if form.is_valid():
                user = request.user
                user.bio=form.cleaned_data['bio']
                user.location=form.cleaned_data['location']

                if  photo:
                   thumpnail_image= thumpnail(photo)
                   user.profile_pic = thumpnail_image

                user.save()
                return redirect('profile',request.user.ui)
            else:
                user = request.user
                form = ProfileInfo(instance=user)
                return render (request,'accounts/editprofile.html',{'form':form})
        else:
            user = request.user
            form = ProfileInfo(instance=user)
            profile=form
            context={
                        'profile':profile,
                    }
            return render (request,'accounts/editprofile.html',context)

@login_required       
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
                return redirect('profile',request.user.ui)
            else:
                user = request.user
                form = EducationForm(instance=user)
                return render (request,'accounts/editprofile.html',{'form':form})
        else:
            user = request.user
            form = EducationForm(instance=user)
            profile=form
            context={
                        'form':profile,
                    }
            return render (request,'accounts/editprofile.html',context)

@login_required
def change_email(request):
    user = request.user
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST or None,user=user)

        if form.is_valid():
            user = request.user
            password = request.POST.get('password')
            if password:
                if user.check_password(password):
                    email = request.POST.get('email')
                    phone_number = request.POST.get('phonenumber')

                    if email:
                        if email == request.user.email:
                             pass
                        else:
                            if CustomUser.objects.filter(email=email).exists():
                                 pass
                            else:
                                user.email = email
                                user.save()
                                messages.success(request, 'Email Updated Succesfully')
                    else:
                        pass
                    if phone_number:
                        if phone_number != request.user.phonenumber:
                            if CustomUser.objects.filter(phonenumber=phone_number).exists():
                                   pass
                            else:
                                user.phonenumber = phone_number
                                user.save()
                                messages.success(request, 'Phone Number Updated Succesfully')      
                                                     
                else:
                    messages.error(request,('Invalid Password'))
                
                return redirect('change_email') 

    else:
        form = ChangeEmailForm(user=user)
    return render(request, 'accounts/editprofile.html', {'form': form})

#signup user 
class SignupWizard(SessionWizardView):
    form_list = [EmailForm,PasswordForm,PersonalInfoFormOne]
    template_name = 'accounts/emailform.html'
   

    def done(self, form_list, **kwargs):

        token = str(uuid.uuid4())
        unique_id=str(uuid.uuid4().hex)[:8]
        first_name=form_list[2].cleaned_data['first_name']
        last_name=form_list[2].cleaned_data['last_name']
        
        if form_list[0].cleaned_data['email'] or form_list[0].cleaned_data['phonenumber']:
            pass
        else:
            raise forms.ValidationError('At least one of email or phone number must be provided')
        user = CustomUser.objects.create_user(
        email=form_list[0].cleaned_data['email'],
        phonenumber=form_list[0].cleaned_data['phonenumber'],
        password=form_list[1].cleaned_data['password1'],
        first_name=form_list[2].cleaned_data['first_name'],
        last_name=form_list[2].cleaned_data['last_name'],
        ui=slugify(f"{first_name} {last_name} {unique_id}") ,
        token = token
       )
        
        user.save()
 
        login(self.request,user,backend='django.contrib.auth.backends.ModelBackend')
        if email:
            subject = 'Account Verification My agric Diary'
            message =f'Thank you for registering with us!  Activate your email  address by clicking the following link: https://www.myagricdiary.com/accounts/verify/{token}'
            sendto = user.email
            email(subject=subject,message=message,sendto=sendto)
        return redirect('firstProfile')

class FirstProfile(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))

    form_list = [ProfileInfo,EducationForm]
    template_name = 'accounts/emailform.html'
    
    def done(self, form_list, **kwargs):
        user = self.request.user
        print(form_list)
        user.bio=form_list[0].cleaned_data['bio']
        user.location=form_list[0].cleaned_data['location']
        #user.profile_pic=form_list[0].cleaned_data['profile_pic']
        profilepic= form_list[0].cleaned_data['profile_pic']
        if profilepic:
            user.profile_pic=thumpnail(form_list[0].cleaned_data['profile_pic'])
        user.is_student=form_list[1].cleaned_data['is_student']
        user.course=form_list[1].cleaned_data['course']
        user.instituition=form_list[1].cleaned_data['instituition']
        user.profession =form_list[1].cleaned_data['profession']
        user.company=form_list[1].cleaned_data['company']
        user.save()
        return redirect('articles')
def searchpage(request):
    
     return render (request,'accounts/search.html',)

     
def search_users(request,slug):
    query = slug
    print(query)
    users = CustomUser.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))[:10]
    pages = Company.objects.filter(Q(name__icontains= query))
    data = {'results': []}
    for user in users:
        data['results'].append({
            'type':'user',
            'id': user.ui,
            'text': user.get_full_name(),
            'profilepic':user.profilepic()
        })
    for user in pages:
        data['results'].append({
             'type':'page',
            'id': user.identifier,
            'text': user.name,
            'profilepic':user.logopic()
        })
    return JsonResponse(data)

def email(subject,message,sendto):
            # send email
            subject = subject
            message = message
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [sendto,]
            send_mail( subject, message, email_from, recipient_list )
            context={'email':sendto}
            return 'done'

@login_required
def check_online_status(request):
    user_id = request.GET.get('user_id')
    user = CustomUser.objects.get(id=user_id)
    if user.last_seen:
        time_diff = timezone.now() - user.last_seen
        if time_diff.total_seconds() <= 30:
            return JsonResponse({'is_online': True})
    return JsonResponse({'is_online': False})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/passwordreset.html'
    def get(self, request, *args, **kwargs):
        myform= PassReset()
        return render(request, self.template_name, {'form':myform})

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        phone = request.POST.get('phonenumber')
        if email:
            email_or_phone = email
            is_email= True
        else:
            email_or_phone = phone
            is_email=False

        if email_or_phone:
            # Check if email_or_phone corresponds to an existing user account
            try:
                user = CustomUser.objects.get(email=email_or_phone)
                got_user = True
            except CustomUser.DoesNotExist:
                got_user = False
                try:
                    user =CustomUser.objects.get(phonenumber=email_or_phone)
                    got_user = True
                except CustomUser.DoesNotExist:
                    # Handle invalid input or non-existent user account
                    got_user = False
        if got_user:
            # Generate a password reset token for the user
            token_generator = default_token_generator
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            subject = 'Password Reset on www.myagricdiary.com'

            # Construct the password reset URL
            reset_url = request.build_absolute_uri(reverse_lazy('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))

            # Send the password reset link to the user via email or SMS
            if is_email:
                # Use Django's built-in password reset email functionality
                subject = subject
                message = f'You are receiving this email because you requested a password reset for your user account at www.myagricdiary.com.Please go to the following page and choose a new password: #For security purpose only click the link if you recently requested a password reset. {reset_url}'
                sendto=email
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [sendto,]
                send_mail( subject, message, email_from, recipient_list )
            else:
                try:
                    # Sendinf link via twilio
                    account_sid = 'AC55caa897055964cd534f89f4b9487323'
                    auth_token = '9f836c911f264eb60d9a1e7131a1379e'
                    client = Client(account_sid, auth_token)

                    message = client.messages.create(
                            body=f'You are receiving this email because you requested a password reset for your user account at www.myagricdiary.com.Please go to the following page and choose a new password: #For security purpose only click the link if you recently requested a password reset.{reset_url}',
                            from_='+18565563965',
                            to=phone
                        )
                except:
                     pass
        return redirect('password_reset_done')
def privacy_settings(request):
     return render(request,('accounts/privacy_settings.html'))

def verify_email(request,token):
    try:
            user=CustomUser.objects.get(token=token)
            user.is_verified= True
            user.save()
            messages.success(request, ("Email verified !"))

            return redirect('articles')
    except:
        return HttpResponse('Invalid url')




def thumpnail(image):
    img = Image.open(image)
    max_size = (200, 200)
    img.thumbnail(max_size,Image.ANTIALIAS)
    output = io.BytesIO()
    img.save(output,format='png', quality=60)
    output.seek(0)
    compressed_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', output.getbuffer().nbytes, None)
    return compressed_image

