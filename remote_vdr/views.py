import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from django.conf import settings

from core.http_handlers.utils import get_setting
from core.models import RemoteSystemSettings

from .provider import CustomProvider


class CustomAdapter(OAuth2Adapter):

    VDR_SERVER_OAUTH_BASE_URL = get_setting("remote_system_base_url")
    provider_id = CustomProvider.id

    access_token_url = f"{VDR_SERVER_OAUTH_BASE_URL}/token"
    profile_url = f"{VDR_SERVER_OAUTH_BASE_URL}/users/"
    # TODO: Look into the issues caused by the host.
    authorize_url = f"http://127.0.0.1:9000/auth"

    def complete_login(self, request, app, token, **kwargs):
        headers = {
            "Authorization": f"Bearer {token.token}",
            "Accept": "application/json",
        }
        useremail = kwargs["response"]["useremail"]
        resp = requests.get(
            self.profile_url + f"{useremail}", headers=headers
        )
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(CustomAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(CustomAdapter)
