from django.db import models
from django.conf import settings  # Import settings to access AUTH_USER_MODEL


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')

    def _str_(self):
        return self.name

    def get_registered_users(self):
        """Fetch users who registered via EventRegistration."""
        return self.registrations.all().values_list('user', flat=True)  # Fetch user IDs
