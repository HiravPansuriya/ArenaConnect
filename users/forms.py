from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, GameProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1',
                  'password2', 'is_organizer']

    def clean_email(self):
        """ Ensure email is provided and unique """
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email is required.")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "A user with this email already exists.")
        return email


class OTPVerificationForm(forms.Form):
    """ Form to verify OTP """
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        label="Enter OTP",
        widget=forms.TextInput(attrs={'placeholder': 'Enter 6-digit OTP'})
    )


class GameProfileForm(forms.ModelForm):
    class Meta:
        model = GameProfile
        fields = ['clash_of_clans_username', 'brawl_star_username',
                  'chess_com_username', 'cod_uid']
