from django.urls import path
from .views import organizer_profile, create_event, view_event_details

urlpatterns = [
    path('profile/', organizer_profile, name='organizer_profile'),
    path('create/', create_event, name='create_event'),
    path('event/<int:event_id>/details/',
         view_event_details, name='view_event_details'),
]
