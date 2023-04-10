# app/templatetags/forum_tags.py

from django import template

register = template.Library()

@register.simple_tag
def has_unread_messages(forum, user):
        if user in forum.members.all():
            last_message = forum.forum_messages.order_by('-timestamp').first()
            if last_message and last_message.author != user:
                read_by_users = last_message.read_by.all()
                if user in read_by_users:
                    return False
                else:
                    return  True
            else:
                return  False
        else:False