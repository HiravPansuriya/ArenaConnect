from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.core.mail import send_mail
import requests
from django.conf import settings
from .models import GameProfile
from .forms import CustomUserCreationForm, GameProfileForm
from .game_api import *
import json
import random
import time

CustomUser = get_user_model()  # Get custom user model


# Constants for OTP handling
OTP_EXPIRY_SECONDS = 180  # 3 minutes
RESEND_OTP_WAIT_SECONDS = 30  # 30 seconds


def generate_otp():
    """ Generate a 6-digit OTP """
    return str(random.randint(100000, 999999))


def signup_view(request):
    """ Handles user signup with OTP verification """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Generate and store OTP in session with timestamp
            otp = generate_otp()
            request.session['signup_otp'] = otp
            request.session['signup_email'] = email
            request.session['signup_data'] = request.POST  # Store form data
            # Store OTP creation time
            request.session['otp_created_at'] = time.time()

            # Send OTP via email
            send_mail(
                "Verify Your Email - ArenaConnect",
                f"Your verification code is {otp}. It is valid for {OTP_EXPIRY_SECONDS // 60} minutes.",
                settings.DEFAULT_FROM_EMAIL,  # Uses email from settings
                [email],
                fail_silently=False,
            )

            messages.info(
                request, f"OTP sent to your email. Please enter it within {OTP_EXPIRY_SECONDS // 60} minutes to complete signup.")
            return redirect('verify_otp')

    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})


def resend_otp_view(request):
    """Handles resending OTP via email, resets OTP timer."""
    email = request.session.get('signup_email')

    if not email:
        messages.error(
            request, "No email found. Please restart the signup process.")
        return redirect('signup')

    # Check if user is allowed to request a new OTP (based on cooldown)
    last_resend_time = request.session.get('last_resend_time', 0)
    current_time = time.time()

    if current_time - last_resend_time < RESEND_OTP_WAIT_SECONDS:
        remaining_time = RESEND_OTP_WAIT_SECONDS - \
            (current_time - last_resend_time)
        messages.warning(
            request, f"Please wait {int(remaining_time)} seconds before requesting a new OTP.")
        return redirect('verify_otp')

    # Generate a new OTP and reset the timer
    new_otp = generate_otp()
    request.session['signup_otp'] = new_otp
    request.session['otp_created_at'] = time.time()  # Reset OTP timestamp
    # Update last resend time
    request.session['last_resend_time'] = current_time

    # Send OTP via email
    send_mail(
        "Your ArenaConnect OTP",
        f"Your new OTP for verification is: {new_otp}. It is valid for {OTP_EXPIRY_SECONDS // 60} minutes.",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    messages.success(
        request, f"A new OTP has been sent to your email. Enter it within {OTP_EXPIRY_SECONDS // 60} minutes to complete the verification.")
    return redirect('verify_otp')


def verify_otp_view(request):
    """ Handles OTP verification with expiration check """
    latest_message = None

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('signup_otp')
        email = request.session.get('signup_email')
        otp_created_at = request.session.get('otp_created_at')

        # Check if OTP exists
        if not session_otp or not otp_created_at:
            email = request.session.get('signup_email')
            if email:
                new_otp = generate_otp()
                request.session['signup_otp'] = new_otp
                request.session['otp_created_at'] = time.time()
                send_mail(
                    "Your ArenaConnect OTP",
                    f"Your OTP for verification is: {new_otp}. It is valid for {OTP_EXPIRY_SECONDS // 60} minutes.",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.info(
                    request, "No OTP found. A new OTP has been sent to your email.")
                return redirect('verify_otp')
            else:
                messages.error(
                    request, "No email found. Please restart signup.")
                return redirect('signup')

        # Check if OTP has expired
        if time.time() - otp_created_at > OTP_EXPIRY_SECONDS:
            messages.error(
                request, "OTP expired. Please request a new one by clicking the 'Resend OTP' button.")
            request.session.pop('signup_otp', None)  # Remove expired OTP
            request.session.pop('otp_created_at', None)  # Remove timestamp
            request.session['last_resend_time'] = time.time(
            ) - RESEND_OTP_WAIT_SECONDS  # Allow immediate resend
            return redirect('verify_otp')

        if entered_otp == session_otp:
            # OTP is correct, proceed with user creation
            form_data = request.session.get('signup_data')
            form = CustomUserCreationForm(form_data)

            if form.is_valid():
                user = form.save()
                login(request, user)  # Log in user after signup

                # Clear session data
                request.session.pop('signup_otp', None)
                request.session.pop('signup_email', None)
                request.session.pop('signup_data', None)
                request.session.pop('otp_created_at', None)

                return redirect('organizer_profile' if user.is_organizer else 'profile')

            messages.error(request, "Error creating user. Please try again.")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    # Extract only the latest message for display
    message_list = list(messages.get_messages(request))
    if message_list:
        latest_message = message_list[-1]  # Get only the last message

    return render(request, 'users/verify_otp.html', {'latest_message': latest_message})


def login_view(request):
    """ Handles user login """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log in user
            return redirect('organizer_profile' if user.is_organizer else 'profile')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """ Logs out the user """
    logout(request)
    return redirect('login')


def delete_account_view(request):
    """Deletes the user account and logs them out."""
    if request.user.is_authenticated:
        user = request.user
        logout(request)  # Log the user out
        user.delete()  # Delete the user from the database
        return redirect('home')  # Redirect to homepage or login page

    messages.error(request, "You need to be logged in to delete your account.")
    return redirect('login')


@login_required
def profile_view(request):
    """ Displays and updates user profile and game stats """

    # Ensure request.user is a valid CustomUser instance
    if isinstance(request.user, AnonymousUser) or not isinstance(request.user, CustomUser):
        messages.error(request, "Authentication error! Please log in again.")
        return redirect('login')

    try:
        profile, created = GameProfile.objects.get_or_create(user=request.user)
    except ValueError:
        messages.error(request, "Profile loading failed. Please log in again.")
        return redirect('login')

    form = GameProfileForm(instance=profile)

    if request.method == 'POST':
        form = GameProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            if profile.clash_of_clans_username:
                print(profile.clash_of_clans_username)
                coc_stats = get_clash_of_clans_stats(
                    profile.clash_of_clans_username)
                if coc_stats:
                    profile.clash_of_clans_trophies = coc_stats.get(
                        "trophies", profile.clash_of_clans_trophies)
                    profile.clash_of_clans_town_hall_level = coc_stats.get(
                        "townHallLevel", profile.clash_of_clans_town_hall_level)

            if profile.brawl_star_username:
                print(profile.brawl_star_username)
                brawl_stats = get_brawl_stars_stats(
                    profile.brawl_star_username)
                if brawl_stats:
                    profile.brawl_star_trophies = brawl_stats.get(
                        "trophies", profile.brawl_star_trophies)

            if profile.chess_com_username:
                chess_stats = get_chess_com_stats(profile.chess_com_username)
                print(chess_stats)
                if chess_stats:
                    profile.chess_com_rating = chess_stats.get(
                        "rating", profile.chess_com_rating)

            if profile.cod_uid:
                cod_stats = get_cod_stats(profile.cod_uid)
                print("ddsdjjfjngjfn")
                if cod_stats:
                    profile.cod_kd = cod_stats.get(
                        "kd", profile.cod_kd)

            profile.save()
            messages.success(request, "Profile updated successfully!")

    return render(request, 'users/profile.html', {'form': form, 'profile': profile})


@csrf_exempt
@login_required
def save_usernames(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            profile, created = GameProfile.objects.get_or_create(
                user=request.user)

            profile.clash_of_clans_username = data.get(
                "clash_of_clans_username", "").strip()
            profile.brawl_star_username = data.get(
                "brawl_star_username", "").strip()
            profile.chess_com_username = data.get(
                "chess_com_username", "").strip()
            profile.cod_uid = data.get("cod_uid", "").strip()

            profile.save()
            return JsonResponse({"message": "Usernames saved successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
