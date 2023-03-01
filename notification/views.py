from django.shortcuts import render
from .models import NotificationUser

# Create your views here.
def getnotification(request):
    loggeduser = request.user
    my_notification = NotificationUser.objects.get(user=loggeduser)
    notification = my_notification.mynotification.all().order_by('-time')
    for items in notification:
        items.is_read = True
        items.save()
    context={
        'notification':notification,
    }
    return render (request,'notification/notification.html' ,context)
