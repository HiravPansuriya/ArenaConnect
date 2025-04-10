from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include



def home_view(request):
    return render(request, "home.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("organizers/", include("organizers.urls")),
    path("events/", include("events.urls")),
    # Authentication URLs
    path("signup/", include("django.contrib.auth.urls")),
    path("login/", include("django.contrib.auth.urls")),
    path("logout/", include("django.contrib.auth.urls")),
    path("profile/", include("users.urls")),

    # Home page route
    path("", home_view, name="home"),
]
