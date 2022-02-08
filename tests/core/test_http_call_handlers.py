from builtins import staticmethod, type

import pytest
import requests
from allauth.socialaccount.models import SocialToken
from django.core.exceptions import FieldDoesNotExist

from core.dataclasses.file_and_folder_dataclasses import (
    VDRFileList,
    VDRFolder,
    VDRSubFolderList,
)
from core.dataclasses.site_dataclasses import VDRSiteDetail, VDRSiteList
from core.dataclasses.utility_dataclasses import VDRServiceError
from core.http_handlers import file_and_folder_http_handlers, site_http_handlers
from core.http_handlers.file_and_folder_http_handlers import (
    download_single_file,
    get_files_in_single_folder,
    get_single_folder_details,
    get_sub_folders_of_single_folder,
    permanently_delete_single_file,
    permanently_delete_single_folder,
    shallow_delete_single_file,
    shallow_delete_single_folder,
)
from core.http_handlers.site_http_handlers import get_all_sites, get_single_site
from core.http_handlers.utils import get_setting
from tests.test_utilities.conftest import (
    generic_user,
    mock_get_bearer_token,
    mock_object_with_error_response,
    mock_object_with_generic_json_response,
    mock_object_with_url_encode_method,
    remote_system_settings,
)
from tests.test_utilities.dataclass_responses import (
    vdr_folder_detail,
    vdr_folder_files_list,
    vdr_folder_subfolders,
    vdr_site_detail,
    vdr_site_list,
)


@pytest.mark.django_db
def test_get_all_sites(
    monkeypatch,
    generic_user,
    vdr_site_list,
    mock_get_bearer_token,
    mock_object_with_generic_json_response,
    remote_system_settings,
):
    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "get", mock_object_with_generic_json_response)
    monkeypatch.setattr(site_http_handlers, "parse_get_all_sites", vdr_site_list)

    result = site_http_handlers.get_all_sites(generic_user)
    assert type(result) == VDRSiteList


@pytest.mark.django_db
def test_get_all_sites_with_query_params(
    monkeypatch,
    generic_user,
    vdr_site_list,
    mock_get_bearer_token,
    mock_object_with_generic_json_response,
    mock_object_with_url_encode_method,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "get", mock_object_with_generic_json_response)
    monkeypatch.setattr(site_http_handlers, "parse_get_all_sites", vdr_site_list)

    result = site_http_handlers.get_all_sites(
        generic_user, mock_object_with_url_encode_method
    )
    assert type(result) == VDRSiteList


@pytest.mark.django_db
def test_get_all_sites_error_response(
    monkeypatch,
    generic_user,
    mock_get_bearer_token,
    mock_object_with_error_response,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "get", mock_object_with_error_response)

    result = site_http_handlers.get_all_sites(generic_user)
    assert type(result) == VDRServiceError


@pytest.mark.django_db
def test_get_single_site_detail(
    monkeypatch,
    generic_user,
    vdr_site_detail,
    mock_get_bearer_token,
    mock_object_with_generic_json_response,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "get", mock_object_with_generic_json_response)
    monkeypatch.setattr(site_http_handlers, "parse_get_single_site", vdr_site_detail)

    result = site_http_handlers.get_single_site(generic_user, 4)
    assert type(result) == VDRSiteDetail


@pytest.mark.django_db
def test_get_single_site_detail_error_response(
    monkeypatch,
    generic_user,
    mock_get_bearer_token,
    mock_object_with_error_response,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "get", mock_object_with_error_response)

    result = site_http_handlers.get_single_site(generic_user, 4)
    assert type(result) == VDRServiceError


@pytest.mark.django_db
def test_get_single_folder_details(
    monkeypatch,
    generic_user,
    vdr_folder_detail,
    mock_get_bearer_token,
    mock_object_with_generic_json_response,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "get", mock_object_with_generic_json_response)
    monkeypatch.setattr(
        file_and_folder_http_handlers, "parse_get_folder_details", vdr_folder_detail
    )

    result = file_and_folder_http_handlers.get_single_folder_details(generic_user, 1234)
    assert type(result) == VDRFolder


@pytest.mark.django_db
def test_get_single_folder_details_error_response(
    monkeypatch,
    generic_user,
    mock_get_bearer_token,
    mock_object_with_error_response,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "get", mock_object_with_error_response)

    result = file_and_folder_http_handlers.get_single_folder_details(generic_user, 4)
    assert type(result) == VDRServiceError


@pytest.mark.django_db
def test_get_sub_folders_of_single_folder(
    monkeypatch,
    generic_user,
    vdr_folder_subfolders,
    mock_get_bearer_token,
    mock_object_with_generic_json_response,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "get", mock_object_with_generic_json_response)
    monkeypatch.setattr(
        file_and_folder_http_handlers,
        "parse_get_single_folder_subfolders",
        vdr_folder_subfolders,
    )

    result = file_and_folder_http_handlers.get_sub_folders_of_single_folder(
        generic_user, 1234
    )
    assert type(result) == VDRSubFolderList


@pytest.mark.django_db
def test_get_sub_folders_of_single_folder_error_response(
    monkeypatch,
    generic_user,
    mock_get_bearer_token,
    mock_object_with_error_response,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "get", mock_object_with_error_response)

    result = file_and_folder_http_handlers.get_sub_folders_of_single_folder(
        generic_user, 4
    )
    assert type(result) == VDRServiceError


@pytest.mark.django_db
def test_get_files_in_single_folder(
    monkeypatch,
    generic_user,
    vdr_folder_files_list,
    mock_get_bearer_token,
    mock_object_with_generic_json_response,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "get", mock_object_with_generic_json_response)
    monkeypatch.setattr(
        file_and_folder_http_handlers,
        "parse_get_single_folder_subfolders",
        vdr_folder_files_list,
    )

    result = file_and_folder_http_handlers.get_sub_folders_of_single_folder(
        generic_user, 1234
    )
    assert type(result) == VDRFileList


@pytest.mark.django_db
def test_get_files_in_single_folder_error_response(
    monkeypatch,
    generic_user,
    mock_get_bearer_token,
    mock_object_with_error_response,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "get", mock_object_with_error_response)

    result = file_and_folder_http_handlers.get_sub_folders_of_single_folder(
        generic_user, 4
    )
    assert type(result) == VDRServiceError


@pytest.mark.django_db
def test_shallow_delete_single_file(
    monkeypatch,
    generic_user,
    mock_get_bearer_token,
    mock_object_with_generic_json_response,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "delete", mock_object_with_generic_json_response)

    result = file_and_folder_http_handlers.shallow_delete_single_file(
        generic_user, 1234
    )
    assert result.status_code == 200


@pytest.mark.django_db
def test_permanently_delete_single_file(
    monkeypatch,
    generic_user,
    mock_get_bearer_token,
    mock_object_with_generic_json_response,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "delete", mock_object_with_generic_json_response)

    result = file_and_folder_http_handlers.shallow_delete_single_file(
        generic_user, 1234
    )
    assert result.status_code == 200


@pytest.mark.django_db
def test_shallow_delete_single_folder(
    monkeypatch,
    generic_user,
    mock_get_bearer_token,
    mock_object_with_generic_json_response,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "delete", mock_object_with_generic_json_response)

    result = file_and_folder_http_handlers.shallow_delete_single_folder(
        generic_user, 1234
    )
    assert result.status_code == 200


@pytest.mark.django_db
def test_permanently_delete_single_folder(
    monkeypatch,
    generic_user,
    mock_get_bearer_token,
    mock_object_with_generic_json_response,
    remote_system_settings,
):

    monkeypatch.setattr(SocialToken.objects, "get", mock_get_bearer_token)
    monkeypatch.setattr(requests, "delete", mock_object_with_generic_json_response)

    result = file_and_folder_http_handlers.permanently_delete_single_folder(
        generic_user, 1234
    )
    assert result.status_code == 200


@pytest.mark.django_db
def test_get_settings(remote_system_settings):
    base_url = get_setting("remote_system_base_url")
    assert base_url == "http://system.com/system"


@pytest.mark.django_db
def test_get_wrong_setting(remote_system_settings):
    with pytest.raises(FieldDoesNotExist):
        silly_setting = get_setting("foo_bar")
