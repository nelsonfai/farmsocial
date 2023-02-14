
from Friends.models import Network
from account.models import CustomUser
from django.db.models import Q


def friendSuggestions(request):
        if request.user.is_authenticated:
            user = request.user
            # get network
            network = Network.objects.get(user=request.user)
            friendsuggestions= suggestions(request,network=network)
            return {'friendsuggestions':friendsuggestions,'mynetwork':network}
        
        else:
                return {}


def suggestions(request, network):
     # Get the current user's profile
    #profile = user
    # Get the list of friends for the current user
    friends = network.following.all()
    user=request.user
    # Find users who are not friends with the current user and have similar interests
    print(friends)
    suggestions =Network.objects.filter(
        following__in = friends).exclude(id=network.id).distinct()
    return suggestions