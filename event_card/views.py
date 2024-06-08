from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Event, Like
from django.contrib.auth.decorators import login_required

@login_required
def index_view(request):
    events = Event.objects.all()
    user_likes = {}
    if request.user.is_authenticated:
        user_likes = {event.id: event.like_set.filter(user=request.user).exists() for event in events}
    
    context = {
        'events': events,
        'user_likes': user_likes,
    }
    return render(request, 'index.html', context)

@login_required
def like_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    liked = False

    like, created = Like.objects.get_or_create(user=user, event=event)
    if created:
        event.likes += 1
        liked = True
    else:
        event.likes -= 1
        like.delete()

    event.save()

    return JsonResponse({'message': 'Liked' if liked else 'Unliked', 'likes': event.likes})
