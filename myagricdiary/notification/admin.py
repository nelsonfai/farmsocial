from django.contrib import admin
from .models import Notification,NotificationUser
# Register your models here.
admin.site.register(NotificationUser)
admin.site.register(Notification)