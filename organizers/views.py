from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from events.models import EventRegistration
from .forms import EventForm
from .models import Event


@login_required
def organizer_profile(request):
    events = Event.objects.filter(organizer=request.user)
    return render(request, 'organizers/profile.html', {'events': events})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('organizer_profile')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})


@login_required
def view_event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Fetch users who registered for this event
    registered_users = EventRegistration.objects.filter(
        event=event).select_related('user')

    return render(request, 'organizers/view_details.html', {'event': event, 'registered_users': [reg.user for reg in registered_users]})
