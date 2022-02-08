import json
import os
from builtins import staticmethod, type

import pytest
from django.contrib.auth import get_user_model

from core.dataclasses.file_and_folder_dataclasses import (
    VDRFile,
    VDRFileList,
    VDRFolder,
    VDRSubFolderList,
)
from core.dataclasses.site_dataclasses import (
    VDRSite,
    VDRSiteCategory,
    VDRSiteDetail,
    VDRSiteList,
    VDRSiteModule,
)


@pytest.fixture
def vdr_site_list_json_response():
    with open("tests/test_utilities/json_files/site_list.json", "r") as f:
        return json.loads(f.read())


@pytest.fixture
def vdr_site_detail_json_response():
    with open("tests/test_utilities/json_files/site_detail.json", "r") as f:
        return json.loads(f.read())


@pytest.fixture
def vdr_folder_detail_json_response():
    with open("tests/test_utilities/json_files/folder_detail.json", "r") as f:
        return json.loads(f.read())


@pytest.fixture
def vdr_subfolders_json_response():
    with open("tests/test_utilities/json_files/folder_subfolders.json", "r") as f:
        return json.loads(f.read())


@pytest.fixture
def vdr_files_in_folder_json_response():
    with open("tests/test_utilities/json_files/files_in_folder.json", "r") as f:
        return json.loads(f.read())
