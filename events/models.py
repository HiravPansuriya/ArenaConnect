from django.db import models
from users.models import CustomUser
from organizers.models import Event


class EventRegistration(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event', 'user')  # Prevent duplicate registrations

    def _str_(self):
        return f"{self.user.username} registered for {self.event.name}"
