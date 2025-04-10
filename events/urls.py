from django.urls import path
from .views import events_list, register_event

urlpatterns = [
    path('', events_list, name='events_list'),
    path('register/<int:event_id>/', register_event, name='register_event'),
]
