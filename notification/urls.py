from django.urls import path
from notification import views



urlpatterns = [
    path('',views.getnotification, name='notification'),
]
