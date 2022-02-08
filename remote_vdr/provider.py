from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class CustomAccount(ProviderAccount):
    pass


class CustomProvider(OAuth2Provider):

    id = "remote_vdr"
    name = "OAuth2 Provider"
    account_class = CustomAccount

    def extract_uid(self, data):
        return str(data["userid"])

    def extract_common_fields(self, data):
        return dict(
            email=data["email"],
            first_name=data["firstname"],
            last_name=data["lastname"],
        )

    # def get_default_scope(self):
    #     pass


providers.registry.register(CustomProvider)
