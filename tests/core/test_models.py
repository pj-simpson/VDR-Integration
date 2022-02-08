import pytest
from django.core.exceptions import ValidationError

from core.models import RemoteSystemSettings
from tests.test_utilities.conftest import remote_system_settings_factory


@pytest.mark.django_db
def test_remote_system_settings_model(remote_system_settings_factory):
    remote_settings = remote_system_settings_factory()
    assert len(RemoteSystemSettings.objects.all()) == 1


@pytest.mark.django_db
def test_remote_system_settings_model_singleton(remote_system_settings_factory):
    remote_settings = remote_system_settings_factory
    remote_settings_override = remote_system_settings_factory(
        base="https:///second.com/second",
        key="987655362713",
        secret="213782816",
        bucket="new-bucket",
    )
    assert len(RemoteSystemSettings.objects.all()) == 1
