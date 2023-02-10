from django.http import JsonResponse
from django.shortcuts import render
from .models import Network
from account.models import CustomUser
# Create your views here.
def follow(request,slug):
    
    targetuser = CustomUser.objects.get(id=slug)
    users_network = Network.objects.get(user=targetuser)
    my_network = Network.objects.get(user=request.user)

    # follow = add me to list of users followers
    users_network.follower.add(request.user)

    # add user to my following list
    my_network.following.add(targetuser)
    print('followed ....')
    return JsonResponse({'data':'unfollow'})



def unfollow (request,slug):
    targetuser = CustomUser.objects.get(id=slug)
    users_network = Network.objects.get(user=targetuser)
    my_network = Network.objects.get(user=request.user)

    # follow = add me to list of users followers
    users_network.follower.remove(request.user)

    # add user to my following list
    my_network.following.remove(targetuser)
    print('un followed ')
    return JsonResponse({'data':'follow'})
