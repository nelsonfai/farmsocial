from .models import Thread,ChatMessage

def get_unread_messages_count(request):
    if  request.user.is_authenticated:
        user= request.user
        # Get all threads involving the user
        threads = Thread.objects.by_user(user=user)
        
        # Count the number of unread messages in all threads involving the user
        count = ChatMessage.objects.filter(
            thread__in=threads,  # Filter by threads involving the user
            user__ne=user,  # Filter out messages sent by the user
            is_read=False,  # Filter by unread messages
        ).count()
        
        return {'unread':count}
    else:
        return{}
