from django.contrib import admin
from .models import CustomUser,GameProfile
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(GameProfile)