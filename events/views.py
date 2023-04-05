from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.


def events(request):
    return render(request,'events/events.html')