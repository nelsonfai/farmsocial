from django.urls import path
from . import views

urlpatterns = [
 
    path('follow/<slug:slug>',views.follow, name='follow'),
    path('unfollow/<slug:slug>',views.unfollow, name='unfollow'),
  
]
