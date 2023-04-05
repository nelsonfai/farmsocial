from django.urls import path
from . import views



urlpatterns = [
    path('',views.events, name='events'),
    path('create_event',views.create, name='create_event'),

    #path('query/',views.aiChat_room, name='ai_bot_search'),
]
