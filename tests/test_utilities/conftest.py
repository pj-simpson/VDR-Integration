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
from core.models import RemoteSystemSettings
from core.site_migration.utilities.utils import (
    FolderContents,
    FolderContentsForHardDelete,
    FolderContentsForLocal,
    FolderContentsForRemote,
    FolderContentsForSoftDelete,
)
from reporting.models import Report, ReportLine


@pytest.fixture
def generic_user():
    def _generic_user():
        return get_user_model().objects.create_user("blah@rah.com", "password")

    return _generic_user


@pytest.fixture
def remote_system_settings():
    return RemoteSystemSettings.objects.create(
        remote_system_base_url="http://system.com/system",
        aws_access_key_id="123456789",
        aws_secret_access_key="987654321",
        aws_bucket_name="system-bucket",
    )


@pytest.fixture
def remote_system_settings_factory():
    def _remote_system_settings(
        base="http://system.com/system",
        key="123456789",
        secret="987654321",
        bucket="system-bucket",
    ):
        return RemoteSystemSettings.objects.create(
            remote_system_base_url=base,
            aws_access_key_id=key,
            aws_secret_access_key=secret,
            aws_bucket_name=bucket,
        )

    return _remote_system_settings


@pytest.fixture
def report_factory():
    def _report(
        root_folder_name="Testing a Folder",
    ):
        return Report.objects.create(root_folder_name=root_folder_name)

    return _report


@pytest.fixture
def report_line_factory():
    def _report_line(
        root_folder_name="Testing a Folder",
    ):
        report = Report.objects.create(root_folder_name=root_folder_name)
        return ReportLine.objects.create(line="Testing a line", report=report)

    return _report_line


class MockSuccessResponse:
    status_code = 200

    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


@pytest.fixture
def mock_object_with_generic_json_response():
    def _mock_generic_json_response(*args, **kwargs):
        mock = MockSuccessResponse()
        return mock

    return _mock_generic_json_response


class MockFailureResponse:
    status_code = 403
    text = "This is an error message"


@pytest.fixture
def mock_object_with_error_response():
    def _mock_object_with_error_response(*args, **kwargs):
        mock = MockFailureResponse()
        return mock

    return _mock_object_with_error_response


@pytest.fixture
def mock_get_bearer_token():
    def _mock_get_bearer_token(*args, **kwargs):
        return "fake-bearer-token"

    return _mock_get_bearer_token


@pytest.fixture
def mock_object_with_url_encode_method():
    class MockObject:
        @staticmethod
        def urlencode():
            return "filterby=recent&status=active"

    return MockObject


@pytest.fixture
def mock_create_directory():
    def _mock_create_directory(*args, **kwargs):
        return True

    return _mock_create_directory


@pytest.fixture
def mock_get_path():
    def _mock_get_path(*args, **kwargs):
        return "root/next level/SiteName/Folder1/Just a folder name"

    return _mock_get_path


@pytest.fixture
def folder_contents_object():
    def _folder_contents_object(folder_id, local_path=None, vdr_path=None):
        user = get_user_model().objects.create_user("blah@rah.com", "password")
        folder_contents = FolderContents(
            user=user.id,
            folder_id=folder_id,
            local_path=local_path,
            vdr_path=vdr_path,
        )
        return folder_contents

    return _folder_contents_object


@pytest.fixture
def folder_contents_object_for_local():
    def _folder_contents_object_for_local(folder_id, local_path=None, vdr_path=None):
        user = get_user_model().objects.create_user("blah@rah.com", "password")
        folder_contents_for_local = FolderContentsForLocal(
            user=user.id,
            folder_id=folder_id,
            local_path=local_path,
            vdr_path=vdr_path,
        )
        return folder_contents_for_local

    return _folder_contents_object_for_local


@pytest.fixture
def folder_contents_object_for_remote():
    def _folder_contents_object_for_remote(folder_id, local_path=None, vdr_path=None):
        user = get_user_model().objects.create_user("blah@rah.com", "password")
        folder_contents_for_remote = FolderContentsForRemote(
            user=user.id,
            folder_id=folder_id,
            local_path=local_path,
            vdr_path=vdr_path,
        )
        return folder_contents_for_remote

    return _folder_contents_object_for_remote


@pytest.fixture
def folder_contents_object_for_soft_delete():
    def _folder_contents_object_for_soft_delete(
        folder_id, local_path=None, vdr_path=None
    ):
        user = get_user_model().objects.create_user("blah@rah.com", "password")
        folder_contents_for_soft_delete = FolderContentsForSoftDelete(
            user=user.id,
            folder_id=folder_id,
            local_path=local_path,
            vdr_path=vdr_path,
        )
        return folder_contents_for_soft_delete

    return _folder_contents_object_for_soft_delete


@pytest.fixture
def folder_contents_object_for_hard_delete():
    def _folder_contents_object_for_hard_delete(
        folder_id, local_path=None, vdr_path=None
    ):
        user = get_user_model().objects.create_user("blah@rah.com", "password")
        folder_contents_object_for_hard_delete = FolderContentsForHardDelete(
            user=user.id,
            folder_id=folder_id,
            local_path=local_path,
            vdr_path=vdr_path,
        )
        return folder_contents_object_for_hard_delete

    return _folder_contents_object_for_hard_delete
