from django.shortcuts import render, redirect
from .models import Event
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

@login_required
def index_view(request):
    events = Event.objects.all()
    return render(request, 'index.html', {'events': events})


