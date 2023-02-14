from django.dispatch import Signal
from django.dispatch import receiver
from .models import Notification,NotificationUser

notification_signal = Signal(providing_args=["message", "trigger", "target"])

@receiver(notification_signal)
def create_notification(message, target, trigger,**kwargs):
   new_notification = Notification.objects.create(message=message, trigger=trigger, target=target)
   receiver = NotificationUser.objects.get(user=target)
   receiver.mynotification.add(new_notification)


