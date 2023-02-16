from django.urls import path
from . import views



urlpatterns = [
    path('',views.chat, name='chatlobby'),
    path('chatroom/<slug:slug>',views.chat_room, name='chatroom'),
    path('createchat/<slug:slug>',views.createchat, name='createchat'),
    path('search-chat',views.search_chat, name='search_chat'),
    path('sendmessage/',views.sendmessage, name='sendmessage'),
]
