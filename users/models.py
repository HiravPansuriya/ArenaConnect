from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_organizer = models.BooleanField(default=False)

class GameProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    clash_of_clans_username = models.CharField(max_length=100, blank=True, null=True)
    clash_of_clans_trophies = models.IntegerField(blank=True, null=True)
    clash_of_clans_town_hall_level = models.IntegerField(blank=True, null=True)
    brawl_star_username = models.CharField(max_length=100, blank=True, null=True)
    brawl_star_trophies = models.FloatField(blank=True, null=True)
    chess_com_username = models.CharField(max_length=100, blank=True, null=True)
    chess_com_rating = models.IntegerField(blank=True, null=True)
    cod_uid = models.CharField(max_length=100, blank=True, null=True)
    cod_kd = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Game Profile"
