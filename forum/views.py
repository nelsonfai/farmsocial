# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Forum,Message
from .forms import CreateForumForm
import uuid
from django.utils.text import slugify
from django.http import JsonResponse
from django.db.models import Sum

@login_required
def create_forum(request):
    if request.method == 'POST':
        form = CreateForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.created_by=request.user
            unique_id=str(uuid.uuid4().hex)[:8]
            name=forum.topic[:20]
            identifier=slugify(f"{name}-{unique_id}") 
            forum.identifier=identifier
            forum.save()
            messages.success(request, 'Forum created successfully!')
            return redirect('forums')
    else:
        form = CreateForumForm()
    return render(request, 'forum/create_forum.html', {'form': form})

@login_required
def join_forum(request):
    forum_id=request.GET.get('forum')
    forum = get_object_or_404(Forum,identifier=forum_id)
    if request.user in forum.members.all():
                forum.members.remove(request.user)
                status='removed'
    else:
                forum.members.add(request.user)
                status='joined'

    return JsonResponse({'data':status})

""" 
@login_required
def delete_forum(request):
    if request.method == 'POST':
        form = DeleteForumForm(request.POST)
        if form.is_valid():
            forum_id = form.cleaned_data['forum_id']
            forum = get_object_or_404(Forum, id=forum_id)
            if request.user == forum.created_by:
                forum.delete()
                messages.success(request, 'Forum deleted successfully!')
            else:
                messages.error(request, 'You cannot delete this forum as you are not the owner.')
            return redirect('home')
    else:
        form = DeleteForumForm()
    return render(request, 'delete_forum.html', {'form': form})
"""
def forums(request):
    filter = request.GET.get('filter')
    if filter == 'myforums':
        forums = Forum.objects.filter(members=request.user)
    else:
        forums = Forum.objects.all()
    return render (request,'forum/forums.html', {'forums':forums})
def forum_room(request,slug):
    forum=Forum.objects.get(identifier=slug)
    messages = forum.forum_messages.order_by('-upvote')
    last_message = forum.forum_messages.order_by('-timestamp').first()
    if last_message:
        last_message.read_by.add(request.user)

    return render (request,'forum/forum.html', {'forum':forum,'forummessages':messages})

def messaging_room(request,slug):
    forum = Forum.objects.get(identifier=slug).prefetch_related('forum_messages')

def send_message(request):
          id =request.POST.get('forum')
          forum= Forum.objects.get(identifier=id)
          text = request.POST.get('message')
          message = Message.objects.create(forum=forum,content=text,author=request.user)
          data={
                'id':message.id,
                'upvote':message.upvote
          }
          return JsonResponse({'data':data})
def upvote(request):
          id =request.GET.get('msg_id')
          message = Message.objects.get(id=id)
          message.upvote +=1
          message.save()
          return JsonResponse({'data':f'{message.upvote}'})
def deleteMessage(request):
    id =request.GET.get('msg_id')
    message = Message.objects.get(id=id)
    if message.author == request.user:
         message.delete()
         status='Deleted' 
    else:
         status='Not permitted to delete this message'  
    return JsonResponse({'data':status})

