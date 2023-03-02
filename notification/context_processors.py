from .models import NotificationUser
from Friends.models import Network


def notificationCount(request):
        if  request.user.is_authenticated:
            user = request.user
            #notification = NotificationUser.objects.get(user = user)
            #count = notification.mynotification.all().filter(is_read = False)
            return {'count':0,'mypages':user.company_admin.all()}
        
        else:
                return {}
