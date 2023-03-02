from .models import Notification,NotificationUser
from celery import Celery
from account.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from feed.models import Articles
from marketplace.models import ProductItem
from Friends.models import Network

app = Celery('tasks', broker='redis://localhost:6379/0', result_backend='redis://localhost:6379/0')

@app.task
@receiver(post_save,sender=Articles)
def send_message(created ,instance ,**kwargs):
        if created:
            notify(instance)

@app.task
@receiver(post_save,sender=ProductItem)
def productnotify(created ,instance ,**kwargs):
        if created:
            productnotify(instance)


@app.task
def notify(instance):
    if instance.author:
        followers= instance.author.myfollowing.follower.all()
        message= f'{instance.author.get_full_name()} posted an article just now check it out'
        url = f'/{instance.slug}'
        if followers:
            new_notification=Notification.objects.create(message=message,url=url,trigger=instance.author)
            for follower in followers: 
                follower.usernotification.mynotification.add(new_notification)

    elif instance.company:
        followers= instance.company.pagefollowers.all()
        message= f'{instance.company.name} posted an article just now check it out'
        url = f'/{instance.slug}'
        if followers:
            new_notification=Notification.objects.create(message=message,url=url,trigger_page=instance.company)
            for follower in followers: 
                follower.usernotification.mynotification.add(new_notification)
    else:
         pass

@app.task       
def productnotify(instance):
    if instance.user_profile:
        followers= instance.user_profile.myfollowing.follower.all()
        message= f'{instance.user_profile.get_full_name()} posted a new product check it out'
        url = f'/market/product/{instance.id}'
        if followers:
            new_notification=Notification.objects.create(message=message,url=url,trigger=instance.user_profile)
            for follower in followers: 
                follower.usernotification.mynotification.add(new_notification)

    elif instance.companypage:
        followers= instance.companypage.pagefollowers.all()
        message= f'{instance.companypage.name} posted a new product check it out'
        url = f'/market/product/{instance.id}'
        if followers:
            new_notification=Notification.objects.create(message=message,url=url,trigger_page=instance.companypage)
            for follower in followers: 
                follower.usernotification.mynotification.add(new_notification)
    else:
         pass


#should be in the signal.py 
@receiver(post_save,sender=CustomUser)
def create_notification(created ,instance ,**kwargs):
        if created:
            notificationuser = NotificationUser.objects.create(user=instance)


#should be in the signal.py 
@receiver(post_save,sender=CustomUser)
def create_network(created ,instance ,**kwargs):
        if created:
            network = Network.objects.create(user=instance)