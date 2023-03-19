from .models import NotificationUser
from Friends.models import Network

from django.views.decorators.cache import cache_page

# Create your views here.
@cache_page(60 * 5) # cache for 5 minutes

def notificationCount(request):
        if  request.user.is_authenticated:
            user = request.user
            notification = NotificationUser.objects.get(user = user)
            count = notification.mynotification.all().filter(is_read = False)
            return {'count':count.count,'mypages':user.company_admin.all()}
        
        else:
                return {}
