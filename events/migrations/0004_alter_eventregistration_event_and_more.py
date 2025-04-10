# Generated by Django 5.1.7 on 2025-03-09 06:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_initial'),
        ('organizers', '0003_alter_event_name_alter_event_organizer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregistration',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='organizers.event'),
        ),
        migrations.AlterUniqueTogether(
            name='eventregistration',
            unique_together={('event', 'user')},
        ),
    ]
