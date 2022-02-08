from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm, PasswordInput

from core.models import RemoteSystemSettings


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )


class SettingsForm(ModelForm):
    class Meta:
        model = RemoteSystemSettings
        fields = "__all__"
        widgets = {
            "aws_access_key_id": PasswordInput(render_value=True),
            "aws_secret_access_key": PasswordInput(render_value=True),
        }
