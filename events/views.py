from calendar import day_name
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, EventRegistration
from django.db.models import Q


def events_list(request):
    event_name = request.GET.get('game_name', '').strip()
    date = request.GET.get('date', '').strip()
    events = Event.objects.all()

    if event_name:
        events = events.filter(name__icontains=event_name)
    if date:
        events = events.filter(date=date)

    return render(request, 'events/events.html', {'events': events, 'game_name': event_name, 'date': date})


@login_required(login_url="/profile/login/")
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the user is already registered for the event
    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        return render(request, 'events/register.html', {'event': event, 'message': 'You are already registered for this event.'})

    # Register the user for the event
    EventRegistration.objects.create(event=event, user=request.user)

    return render(request, 'events/register.html', {'event': event, 'message': 'You have successfully registered for the event.'})
