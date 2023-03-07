from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from chat.models import Thread,ChatMessage
from django.db.models import Q
from django.http import JsonResponse


from account.models import CustomUser
#from django.contrib.auth.models import User

# Create your views here.


@login_required
def chat (request):
    threads =Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    unread_counts = []
    for thread in threads:
        unread_count = thread.chatmessage_thread.filter(is_read=False).exclude(user= request.user).count()
        unread_counts.append(unread_count)
    context = {
        'threads': threads,
        'unread_counts': unread_counts

    }
    return render(request, 'chat/chat.html', context)

@login_required   
def chat_room(request,slug):
    #
    thread_room = Thread.objects.filter(id=slug).prefetch_related('chatmessage_thread').order_by('timestamp')
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    #thread_room = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    for chat in thread_room[0].chatmessage_thread.filter(is_read=False):
        chat.is_read=True
        chat.save()
    context = {
        'thread_room': thread_room,
        'threads':threads,
        'activeuser':request.user,
        'threadid':slug
    }
    print(f' in chat room')
    return render(request, 'chat/chat_room.html', context)
@login_required    
def createchat(request,slug):
    print(type(slug))
    user= request.user
    user2 = CustomUser.objects.get(id=slug)
    
    print(type(user.id))
    threads= Thread.objects.filter( Q( first_person = user ) & Q(second_person = user2) | Q( first_person = user2) & Q( second_person = user))
    print(threads)
    if threads.count() > 0:
        slugid=threads[0].id
        return redirect('chatroom', slug=slugid)
    else:
        user = request.user
        second_user=CustomUser.objects.get(id=slug)
        new_thread= Thread(first_person=request.user, second_person=second_user)
        new_thread.save()
        return redirect('chatlobby')

def search_chat(request):
    if request.method=='POST':
        user=request.user
        searched=request.POST.get('search')
        threads= Thread.objects.filter( Q( first_person = user.id ) & Q(second_person__contains=searched) | Q( first_person__contains= searched) & Q( second_person = user.id))
        context = {
            'threads': threads
        }
        return render(request, 'chat/chat.html', context)

def sendmessage(request):
    if request.method=='POST':
        message = request.POST['message']
        id =request.POST['id']
        thread = Thread.objects.get(id=id)
        new =ChatMessage(thread=thread, user=request.user, message=message)
        new.save()
        return JsonResponse({'date':'success'})
    
