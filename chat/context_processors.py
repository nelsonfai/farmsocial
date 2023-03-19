from .models import Thread,ChatMessage
from django.db.models import Q
from django.views.decorators.cache import cache_page

# Create your views here.
@cache_page(60 * 1) # cache for 5 minutes
def get_unread_messages_count(request):
    
    if  request.user.is_authenticated:
        user=request.user
        threads = Thread.objects.filter(Q(first_person=user) | Q(second_person=user))
        count = ChatMessage.objects.filter(
            thread__in=threads,  
            is_read=False 
        ).exclude(user=user).count()
        
        return {'unread':count}
    else:
        return{}
