# forms.py
from django import forms
from .models import Forum

class CreateForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['topic', 'room_description']

class JoinForumForm(forms.Form):
    forum_id = forms.IntegerField()

class UnjoinForumForm(forms.Form):
    forum_id = forms.IntegerField()

class DeleteForumForm(forms.Form):
    forum_id = forms.IntegerField()
