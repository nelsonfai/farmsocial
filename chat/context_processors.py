from .models import Thread,ChatMessage
from django.db.models import Q
def get_unread_messages_count(request):
    if  request.user.is_authenticated:
        user= request.user
        threads = Thread.objects.filter(Q(first_person=user) | Q(second_person=user))
        count = ChatMessage.objects.filter(
            thread__in=threads,  
            is_read=False 
        ).exclude(user=user).count()
        
        return {'unread':count}
    else:
        return{}
