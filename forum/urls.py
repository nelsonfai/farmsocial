from django.urls import path
from . import views



urlpatterns = [
    path('',views.forums, name='forums'),
    path('join_forum',views.join_forum, name='join_forum'),
    path('<slug:slug>',views.forum_room, name='forumroom'),
    path('slug:slug>/message_forum',views.messaging_room, name='messageforum'),
    path('create_form/',views.create_forum, name='createforum'),
    path('sendmessage/',views.send_message, name='sendmessage'),
    path('delete/message',views.deleteMessage, name='deleteforum'),

    path('upvote/message',views.upvote, name='upvote'),

    #path('search-chat',views.search_chat, name='search_forum'),
    #path('sendmessage/',views.sendmessage, name='sendforum'),
]
