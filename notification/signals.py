from django.dispatch import Signal
from django.dispatch import receiver
from .models import Notification,NotificationUser

notification_signal = Signal(providing_args=["message", "trigger", "target","url"])

@receiver(notification_signal)
def create_notification(message, target, trigger,url,**kwargs):
   new_notification = Notification.objects.create(message=message, trigger=trigger,url=url)
   target.usernotification.mynotification.add(new_notification)

