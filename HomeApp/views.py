from collections import Counter
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Event, Like, UserAction
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Prefetch
from django.db.models.functions import Coalesce

def get_filtered_events(query='', user=None, favorites_only=False):
    """Get filtered events based on query and user preferences."""
    events = Event.objects.all()
    
    if query:
        events = events.filter(Q(name__icontains=query) | Q(place__icontains=query))
    
    if favorites_only and user:
        events = events.filter(like__user=user)
    
    return events

def get_user_likes(events, user):
    """Get user likes for events."""
    if not user.is_authenticated:
        return {}
    
    likes = Like.objects.filter(event__in=events, user=user)
    return {like.event_id: True for like in likes}

def calculate_event_statistics(events):
    """Calculate event type statistics."""
    event_types = [event.type for event in events]
    event_type_counts = dict(Counter(event_types))
    total_events = sum(event_type_counts.values())
    
    return {
        'counts': event_type_counts,
        'percentages': {
            event_type: int((count / total_events) * 100)
            for event_type, count in event_type_counts.items()
        }
    }

@login_required
def base_view(request):
    query = request.GET.get('query', '')
    favorites_only = request.GET.get('favorites') == 'true'
    
    # Get filtered events with optimized query
    events = get_filtered_events(query, request.user, favorites_only)
    
    # Get user likes with optimized query
    user_likes = get_user_likes(events, request.user)
    
    # Calculate statistics
    stats = calculate_event_statistics(events)
    
    # Get recent user actions with optimized query
    user_actions = UserAction.objects.select_related('user', 'event').order_by('-timestamp')[:6]
    
    context = {
        'events': events,
        'user_likes': user_likes,
        'event_type_counts': stats['counts'],
        'event_type_percentages': stats['percentages'],
        'query': query,
        'event_count': Event.objects.count(),
        'user_actions': user_actions,
        'form_data': {'username': request.user.username}  # Add form_data for template
    }
    return render(request, 'base.html', context)

@login_required
def like_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    
    like, created = Like.objects.get_or_create(user=user, event=event)
    
    if created:
        event.likes += 1
        UserAction.objects.create(user=user, event=event, action_type='like')
    else:
        event.likes -= 1
        like.delete()
    
    event.save()
    
    return JsonResponse({
        'message': 'Liked' if created else 'Unliked',
        'likes': event.likes
    })

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
    context = {
        'form_data': {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        }
    }
    return render(request, 'profile.html', context)

def details_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    context = {
        'event': event,
        'form_data': {'username': request.user.username} if request.user.is_authenticated else {}
    }
    return render(request, 'details.html', context)

