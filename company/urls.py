from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/<slug:identifier>',views.dashboard, name='dashboard'),
    path('create/',views.create_company, name='create-company'),
    path('followpage/<slug:slug>',views.follow_page, name='followpage'),
    path('companyprofile/<str:slug>/<str:name>', views.company_profile, name='companyprofile'),
]
