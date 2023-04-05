from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import secrets
from django.utils.text import slugify

# Create your views here.
from .forms import EventForm
from company.models import Company
from .models import Events

def events(request):
    filter = request.GET.get('category')
    if filter:
        if filter == 'attending':
            user=request.user
            events = Events.objects.filter(attending=user)

        elif filter == 'myevents':
            user=request.user
            events=Events.objects.filter(user=user)
        else:
            return redirect('events')
    else:
        events = Events.objects.filter(expired=False)
  
    return render(request,'events/events.html',{'events':events})

def create(request):
    if request.method == 'POST':
        details=request.POST.get('description')
        organizer = request.POST.get('organizer')
        form = EventForm(request.POST or None)
        if form.is_valid():
                obj=form.save(commit=False)
                if organizer == "user":
                    user = request.user
                    obj.user=user
                else:
                     company = Company.objects.get(identifier = organizer)
                     obj.page= company
                obj.country= request.user.location
                obj.slug = slug_generator(title=obj.title[:10])
                obj.description=f'<pre>{details}</pre>'
                obj.save()
        
    else:
        form= EventForm()
        return render(request,'feed/add-article.html',{'form':form})




def slug_generator(title):
    new_title = title
  
    random_string = secrets.token_hex(5)
    print(random_string)
    slug_string = " ".join([new_title, random_string])
    slug = slugify(slug_string)
    return slug


def attending(request):
    slug = request.GET.get('event')
    user = request.user
    event = Events.objects.get(slug=slug)
    if user in event.attending.all:
        event.attending.add(request.user)
        status = 'added'
    else:
        event.attending.remove(request.user)
        status='removed'


    return JsonResponse({'comment':status})



     
    
