import pytest
from django.urls import reverse

from core import views
from tests.test_utilities.conftest import remote_system_settings
from tests.test_utilities.dataclass_responses import vdr_site_detail, vdr_site_list


@pytest.mark.django_db
def test_sites_view(client, monkeypatch, vdr_site_list, remote_system_settings):

    monkeypatch.setattr(views, "get_all_sites", vdr_site_list)
    url = reverse("sites")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_site_detail_view(client, monkeypatch, vdr_site_detail, remote_system_settings):

    monkeypatch.setattr(views, "get_single_site", vdr_site_detail)
    url = reverse("site", kwargs={"id": 4})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_settings_view_fresh_form(client):

    url = reverse("settings")
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_settings_view_fresh_form(client, remote_system_settings):

    url = reverse("settings")
    data = {
        "remote_system_base_url": "https://example.com",
        "aws_access_key_id": "123456789",
        "aws_secret_access_key": "0987654321",
        "aws_bucket_name": "bucket-bucket",
    }
    response = client.post(url, data, content_type="application/x-www-form-urlencoded")
    assert response.status_code == 302
