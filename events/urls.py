from django.urls import path
from . import views



urlpatterns = [
    path('',views.events, name='events'),
    #path('query/',views.aiChat_room, name='ai_bot_search'),
]
