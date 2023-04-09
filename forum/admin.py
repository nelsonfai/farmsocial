from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Forum, Message

admin.site.register(Message)
admin.site.register(Forum)


