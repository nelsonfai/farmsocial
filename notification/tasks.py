from .models import Notification,NotificationUser
from celery import Celery
from accounts.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from feed.models import Articles
from marketplace.models import ProductItem
from Friends.models import Network
from django.db.models.signals import post_delete
###

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
    if instance.video:
         pass
    if instance.author:
        followers= instance.author.myfollowing.follower.all()
        message= f'{instance.author.get_full_name()} posted a new article'
        url = f'/{instance.slug}'
        if followers:
            new_notification=Notification.objects.create(message=message,url=url,trigger=instance.author)
            for follower in followers: 
                follower.usernotification.mynotification.add(new_notification)

    elif instance.company:
        followers= instance.company.pagefollowers.all()
        message= f'{instance.company.name} posted a new article'
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
        message= f'{instance.user_profile.get_full_name()} posted a new product '
        url = f'/market/product/{instance.id}'
        if followers:
            new_notification=Notification.objects.create(message=message,url=url,trigger=instance.user_profile)
            for follower in followers: 
                follower.usernotification.mynotification.add(new_notification)

    elif instance.companypage:
        followers= instance.companypage.pagefollowers.all()
        message= f'{instance.companypage.name} posted a new product'
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


@receiver(post_delete, sender=Articles)  # replace Article with the appropriate model
def delete_related_notifications(sender, instance, **kwargs):
    Notification.objects.filter(url=instance.get_absolute_url).delete()

@receiver(post_delete, sender=ProductItem)  # replace Article with the appropriate model
def delete_related_notifications(sender, instance, **kwargs):
    Notification.objects.filter(url=instance.get_absolute_url).delete()



import subprocess
from django.db.models.signals import pre_save
from django.dispatch import receiver
import subprocess
import os
from tempfile import NamedTemporaryFile
from django.core.files import File
import uuid
from io import BytesIO

@receiver(pre_save, sender=Articles)
def compress_video(sender, instance, **kwargs):
    if instance.video:  # check if a video file is uploaded
        # create a temporary file to save the original video
        with NamedTemporaryFile(delete=False) as tmp_file:
            for chunk in instance.video.chunks():
                tmp_file.write(chunk)

        # compress the video using FFmpeg
        output_file = tmp_file.name + '_compressed.mp4'
        subprocess.run(['ffmpeg', '-i', tmp_file.name, '-vcodec', 'libx265', '-crf', '28', '-f', 'mp4', output_file], check=True)

        # read the compressed video file into memory
        with open(output_file, 'rb') as compressed_file:
            compressed_video_data = compressed_file.read()

        # create a BytesIO object from the compressed video data
        compressed_video_data = BytesIO(compressed_video_data)

        # replace the original video file with the compressed video file
        compressed_file_name = f"{instance.video.name.split('.')[0]}_compressed.mp4"
        instance.video.delete(save=False)
        instance.video.save(compressed_file_name, File(compressed_video_data), save=False)

        # delete the temporary files
        os.remove(tmp_file.name)
        os.remove(output_file)
