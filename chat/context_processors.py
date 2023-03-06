from .models import Thread,ChatMessage
from django.db.models import Q
def get_unread_messages_count(request):
    if  request.user.is_authenticated:
        user= request.user
        # Get all threads involving the user
        threads = Thread.objects.filter(Q(first_person=user) | Q(second_person=user))
        # Count the number of unread messages in all threads involving the user
        count = ChatMessage.objects.filter(
            thread__in=threads,  # Filter by threads involving the user
            is_read=False,  # Filter by unread messages
        ).exclude(user=user).count()
        
        return {'unread':count}
    else:
        return{}
