from collections import Counter
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Event, Like, UserAction
from django.contrib.auth.decorators import login_required
from django.db.models import Q
@login_required
def index_view(request):
    query = request.GET.get('query', '')
    events = Event.objects.all()
    if query:
        events = events.filter(Q(name__icontains=query) | Q(place__icontains=query))

    user_likes = {}
    if request.user.is_authenticated:
        user_likes = {event.id: event.like_set.filter(user=request.user).exists() for event in events}
    
    if request.GET.get('favorites') == 'true':
        events = events.filter(like__user=request.user)
    
    event_types = [event.type for event in events]
    event_type_counts = dict(Counter(event_types))
    total_events = sum(event_type_counts.values())

    event_type_percentages = {}

    for event_type, count in event_type_counts.items():
        percentage = (count / total_events) * 100
        event_type_percentages[event_type] = int(percentage)

    event_count = Event.objects.all().count()

    user_actions = UserAction.objects.all().order_by('-timestamp')[:6]  # Get the last 10 actions



    context = {
        'events': events,
        'user_likes': user_likes,
        'event_type_counts': event_type_counts,
        'event_type_percentages': event_type_percentages,
        'query': query,  # Pass the query back to the template
        'event_count':event_count,
        'user_actions': user_actions    
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
        UserAction.objects.create(user=user, event=event, action_type='like')
    else:
        event.likes -= 1
        like.delete()
        # UserAction.objects.create(user=user, event=event, action_type='like')  # Record unliking as well

    event.save()

    return JsonResponse({'message': 'Liked' if liked else 'Unliked', 'likes': event.likes})

@login_required
def share_event(request, event_id, platform):
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    action_type = f'share_{platform}'
    if action_type in dict(UserAction.ACTION_TYPES):
        UserAction.objects.create(user=user, event=event, action_type=action_type)
        return JsonResponse({'message': f'Shared on {platform.capitalize()}'})
    return JsonResponse({'message': 'Invalid platform'}, status=400)


@login_required
def profile_view(request):
    return render(request, 'profile.html')
