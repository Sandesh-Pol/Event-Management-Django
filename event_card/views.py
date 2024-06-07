from django.shortcuts import render, redirect
from .models import Event
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

@login_required
def index_view(request):
    events = Event.objects.all()
    return render(request, 'index.html', {'events': events})

def increment_likes(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.likes += 1
        event.save()
        return JsonResponse({'likes': event.likes})
    return JsonResponse({'error': 'Invalid request'}, status=400)

