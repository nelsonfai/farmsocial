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
            events = Events.objects.filter(attending=user).order_by('start_date')

        elif filter == 'myevents':
            user=request.user
            events=Events.objects.filter(user=user).order_by('start_date')
        else:
            return redirect('events')
    else:
        events = Events.objects.filter(expired=False).order_by('start_date')
  
    return render(request,'events/events.html',{'events':events})

def create(request):
    if request.method == 'POST':
        organizer = request.POST.get('organizer')
        description =request.POST.get('details')
        form = EventForm(request.POST or None)
        if form.is_valid():
                obj=form.save(commit=False)
                obj.description=f'<pre>{description}</pre>'
                if organizer == "user":
                    user = request.user
                    obj.user=user
                else:
                     company = Company.objects.get(identifier = organizer)
                     obj.page= company
                obj.slug = slug_generator(title=obj.title[:10])
                obj.save()
        return redirect('events')
    else:
        form= EventForm()
        options = request.user.company_admin.all()

        return render(request,'events/add-event.html',{'form':form,'options':options})




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
    if event.attending.filter(id=user.id).exists():
        event.attending.remove(request.user)
        status='removed'
    else:

        event.attending.add(request.user)
        status = 'added'

    return JsonResponse({'comment':status})

def delete(request):
    slug = request.GET.get('event')
    event= Events.objects.get(slug=slug)
    if event.user:
        if event.user  == request.user:
            event.delete()
            status='deleted'
    if event.page:
        if event.page.user == request.user:
            event.delete()
            status='deleted'
        
    return JsonResponse({'comment':status})

    
