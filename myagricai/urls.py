from django.urls import path
from . import views



urlpatterns = [
    path('chat/',views.myagricAi, name='ai_room'),
    path('query/',views.aiChat_room, name='ai_bot_search'),
]
