from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from allauth.account.views import LoginView



urlpatterns = [
    
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('signup/', views.SignupWizard.as_view(), name='signup'),
    path('verify/<str:token>', views.verify_email, name = 'verify'),
    path('check_online_status/',views.check_online_status, name='onlinestatus'),

    path('firstprofile/', views.FirstProfile.as_view(), name='firstProfile'),
    path('profile/<slug:slug>',views.profile, name='profile'),
    path('editprofile/name/',views.edit_name, name='editname'),
    path('editprofile/bio/',views.edit_bio, name='editbio'),
    path('editprofile/education/',views.edit_education, name='editeducation'),
    path('searchpage/',views.searchpage, name='searchpage'),

    path('queryusers/<slug:slug>',views.search_users, name='search_users'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('google/login/', LoginView.as_view(
        template_name='accounts/google_login.html', 
        #authentication_method='google',
        extra_context={'title': 'Google Login'}
    ), name='account_signup'),
    
  
]
