from builtins import type

import pytest

from core.data_parsers.file_and_folder_data_parsers import (
    parse_get_files_in_single_folder,
    parse_get_folder_details,
    parse_get_single_folder_subfolders,
)
from core.data_parsers.site_data_parsers import (
    parse_get_all_sites,
    parse_get_single_site,
)
from core.dataclasses.file_and_folder_dataclasses import (
    VDRFileList,
    VDRFolder,
    VDRSubFolderList,
)
from core.dataclasses.site_dataclasses import VDRSiteDetail, VDRSiteList
from tests.test_utilities.json_responses import (
    vdr_files_in_folder_json_response,
    vdr_folder_detail_json_response,
    vdr_site_detail_json_response,
    vdr_site_list_json_response,
    vdr_subfolders_json_response,
)


@pytest.mark.django_db
def test_parse_get_all_sites(vdr_site_list_json_response):
    result = parse_get_all_sites(vdr_site_list_json_response)
    assert type(result) == VDRSiteList


@pytest.mark.django_db
def test_parse_get_single_site_detail(vdr_site_detail_json_response):
    result = parse_get_single_site(vdr_site_detail_json_response)
    assert type(result) == VDRSiteDetail


@pytest.mark.django_db
def test_parse_get_folder_details(vdr_folder_detail_json_response):
    result = parse_get_folder_details(vdr_folder_detail_json_response)
    assert type(result) == VDRFolder


@pytest.mark.django_db
def test_parse_get_single_folder_subfolders(vdr_subfolders_json_response):
    result = parse_get_single_folder_subfolders(vdr_subfolders_json_response)
    assert type(result) == VDRSubFolderList


@pytest.mark.django_db
def test_parse_get_files_in_single_folder(vdr_files_in_folder_json_response):
    result = parse_get_files_in_single_folder(vdr_files_in_folder_json_response)
    assert type(result) == VDRFileList
