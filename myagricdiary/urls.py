"""myagricdiary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
#from .import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import RedirectView
favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

def useragreement(request):
    return render(request,'main/user-agreement.html')

def privacy_policy(request):
    return render(request,'main/privacy.html')
def cookie_policy(request):
    return render(request,'main/cookie.html')

urlpatterns = [
    path('myadmin/main/', admin.site.urls),
    path('my_notification' ,include('notification.urls')),
    path('friends/' ,include('Friends.urls')),
    path('accounts/', include('accounts.urls') ),
    path('events/', include('events.urls') ),
    path('apps/', include('agricapps.urls') ),
    path('', include('feed.urls') ),
    path('market/', include('marketplace.urls') ),
    path('chat/', include('chat.urls') ),
    path('company/', include('company.urls') ),
    path('ai/', include('myagricai.urls') ),
    path('forum/', include('forum.urls') ),

    path('legal/user_agreement/',useragreement, name='useragreement'),
    path('legal/privacypolicy/',privacy_policy, name='privacypolicy'),
    path('legal/cookie_policy/',cookie_policy, name='cookiepolicy'),
    path('favicon.ico', favicon_view),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]
urlpatterns+=staticfiles_urlpatterns()
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
