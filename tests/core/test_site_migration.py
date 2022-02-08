import os

import pytest

from core.site_migration.utilities import utils
from tests.test_utilities.conftest import (
    folder_contents_object,
    folder_contents_object_for_hard_delete,
    folder_contents_object_for_local,
    folder_contents_object_for_remote,
    folder_contents_object_for_soft_delete,
    mock_create_directory,
    mock_get_path,
    mock_object_with_generic_json_response,
    remote_system_settings,
)
from tests.test_utilities.dataclass_responses import (
    vdr_file_detail,
    vdr_folder_detail,
    vdr_folder_files_list,
    vdr_folder_subfolders,
)


@pytest.mark.django_db
def test_folder_contents_object_init(folder_contents_object):

    folder = folder_contents_object(
        123, "Local/Project/SiteName/Folder1", "SiteName/Folder1"
    )
    assert folder.folder_id == 123
    assert folder.user.id == 1
    assert folder.local_path == "Local/Project/SiteName/Folder1"
    assert folder.vdr_path == "SiteName/Folder1"
    assert not folder.folder_details
    assert not folder.subfolders
    assert not folder.files


@pytest.mark.django_db
def test_folder_contents_object_get_folder_details(
    monkeypatch, folder_contents_object, vdr_folder_detail
):

    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)

    folder = folder_contents_object(
        123, "Local/Project/SiteName/Folder1", "SiteName/Folder1"
    )
    folder._get_folder_details()
    assert folder.folder_details


@pytest.mark.django_db
def test_folder_contents_object_initialize_report_writer(
    monkeypatch, folder_contents_object, vdr_folder_detail
):

    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)

    folder = folder_contents_object(
        123, "Local/Project/SiteName/Folder1", "SiteName/Folder1"
    )
    folder._get_folder_details()
    folder._initialize_report_writer()
    assert folder.report is not None
    assert folder.report_id == 1


@pytest.mark.django_db
def test_folder_contents_object_updates_local_path_no_local_path_supplied(
    monkeypatch, folder_contents_object, vdr_folder_detail, mock_get_path
):

    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)
    monkeypatch.setattr(os.path, "join", mock_get_path)

    folder = folder_contents_object(123, "", "SiteName/Folder1")
    folder._get_folder_details()
    folder._update_local_path()
    assert folder.local_path == "root/next level/SiteName/Folder1/Just a folder name"


@pytest.mark.django_db
def test_folder_contents_object_updates_local_path(
    monkeypatch, folder_contents_object, vdr_folder_detail
):

    folder = folder_contents_object(
        123,
        "root/next level/SiteName/Folder1/Just a folder name",
        "SiteName/Folder1/Just a folder name",
    )
    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)
    folder._get_folder_details()
    folder._update_local_path()
    assert (
        folder.local_path
        == "root/next level/SiteName/Folder1/Just a folder name/Just a folder name"
    )


@pytest.mark.django_db
def test_folder_contents_object_updates_vdr_path_no_vdr_path_supplied(
    monkeypatch, folder_contents_object, vdr_folder_detail
):

    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)

    folder = folder_contents_object(123)
    folder._get_folder_details()
    folder._update_vdr_path()
    assert folder.vdr_path == "Just a folder name"


@pytest.mark.django_db
def test_folder_contents_object_updates_vdr_path(
    monkeypatch, folder_contents_object, vdr_folder_detail
):

    folder = folder_contents_object(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )
    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)
    folder._get_folder_details()
    folder._update_vdr_path()
    assert folder.vdr_path == "SiteName/Folder1/Just a folder name"


@pytest.mark.django_db
def test_folder_contents_get_subfolders(
    monkeypatch,
    folder_contents_object,
    vdr_folder_subfolders,
    mock_get_path,
    vdr_folder_detail,
):

    folder = folder_contents_object(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )

    monkeypatch.setattr(
        utils, "get_sub_folders_of_single_folder", vdr_folder_subfolders
    )
    monkeypatch.setattr(os.path, "join", mock_get_path)
    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)

    folder._get_folder_details()
    folder._update_vdr_path()
    folder._update_local_path()
    folder._get_subfolders()
    assert folder.subfolders


@pytest.mark.django_db
def test_folder_contents_get_files(
    monkeypatch,
    folder_contents_object,
    vdr_folder_files_list,
    mock_get_path,
    vdr_folder_detail,
):
    folder = folder_contents_object(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )

    monkeypatch.setattr(utils, "get_files_in_single_folder", vdr_folder_files_list)
    monkeypatch.setattr(os.path, "join", mock_get_path)
    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)

    folder._get_folder_details()
    folder._update_vdr_path()
    folder._update_local_path()
    folder._get_files()
    assert folder.files


@pytest.mark.django_db
def test_folder_contents_has_files_when_files(
    monkeypatch,
    folder_contents_object,
    vdr_folder_files_list,
    mock_get_path,
    vdr_folder_detail,
):

    folder = folder_contents_object(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )

    monkeypatch.setattr(utils, "get_files_in_single_folder", vdr_folder_files_list)
    monkeypatch.setattr(os.path, "join", mock_get_path)
    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)

    folder._get_folder_details()
    folder._update_vdr_path()
    folder._update_local_path()
    folder._get_files()
    assert folder.has_files()


@pytest.mark.django_db
def test_folder_contents_has_files_when_no_files(
    folder_contents_object,
):

    folder = folder_contents_object(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )

    assert not folder.has_files()


@pytest.mark.django_db
def test_folder_contents_has_subfolders_when_subfolders(
    monkeypatch,
    folder_contents_object,
    vdr_folder_subfolders,
    mock_get_path,
    vdr_folder_detail,
):

    folder = folder_contents_object(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )

    monkeypatch.setattr(
        utils, "get_sub_folders_of_single_folder", vdr_folder_subfolders
    )
    monkeypatch.setattr(os.path, "join", mock_get_path)
    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)

    folder._get_folder_details()
    folder._update_vdr_path()
    folder._update_local_path()
    folder._get_subfolders()
    assert folder.has_subfolders()


@pytest.mark.django_db
def test_folder_contents_has_subfolders_when_no_subfolders(folder_contents_object):

    folder = folder_contents_object(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )

    assert not folder.has_subfolders()


@pytest.mark.django_db
def test_folder_contents_prepare_folder_method(
    monkeypatch,
    folder_contents_object,
    vdr_folder_subfolders,
    vdr_folder_files_list,
    mock_get_path,
    vdr_folder_detail,
):

    folder = folder_contents_object(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )

    monkeypatch.setattr(
        utils, "get_sub_folders_of_single_folder", vdr_folder_subfolders
    )
    monkeypatch.setattr(os.path, "join", mock_get_path)
    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)
    monkeypatch.setattr(utils, "get_files_in_single_folder", vdr_folder_files_list)

    folder.prepare_folder()

    assert folder.has_files()
    assert folder.has_subfolders()
    assert folder.vdr_path == "SiteName/Folder1/Just a folder name"
    assert folder.local_path == "root/next level/SiteName/Folder1/Just a folder name"


@pytest.mark.django_db
def test_folder_contents_for_local_get_local_file_path_method(
    monkeypatch,
    folder_contents_object_for_local,
    vdr_folder_detail,
    vdr_file_detail,
):

    folder = folder_contents_object_for_local(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )
    file = vdr_file_detail()

    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)

    folder._get_folder_details()
    folder._update_local_path()
    result = folder._get_local_file_path(file)
    assert result == "root/next level/SiteName/Folder1/Just a folder name/A File.png"


@pytest.mark.django_db
def test_folder_contents_object_for_remote_super_init(
    folder_contents_object_for_remote, remote_system_settings
):

    folder = folder_contents_object_for_remote(
        123, "Local/Project/SiteName/Folder1", "SiteName/Folder1"
    )
    assert folder.s3_client


@pytest.mark.django_db
def test_folder_contents_for_remote_get_remote_file_path_method(
    monkeypatch,
    folder_contents_object_for_remote,
    vdr_folder_detail,
    vdr_file_detail,
):

    folder = folder_contents_object_for_remote(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )
    file = vdr_file_detail()

    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)

    folder._get_folder_details()
    folder._update_vdr_path()
    result = folder._get_remote_file_path(file)
    assert result == "SiteName/Folder1/Just a folder name/A File.png"


@pytest.mark.django_db
def test_folder_contents_for_soft_delete_iterate_over_and_shallow_delete_files(
    monkeypatch,
    folder_contents_object_for_soft_delete,
    vdr_folder_subfolders,
    vdr_folder_files_list,
    mock_get_path,
    vdr_folder_detail,
    mock_object_with_generic_json_response,
):
    folder = folder_contents_object_for_soft_delete(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )
    monkeypatch.setattr(
        utils, "get_sub_folders_of_single_folder", vdr_folder_subfolders
    )
    monkeypatch.setattr(os.path, "join", mock_get_path)
    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)
    monkeypatch.setattr(utils, "get_files_in_single_folder", vdr_folder_files_list)
    monkeypatch.setattr(
        utils, "shallow_delete_single_file", mock_object_with_generic_json_response
    )

    folder.prepare_folder()
    folder.iterate_over_and_shallow_delete_files()


@pytest.mark.django_db
def test_folder_contents_for_soft_delete_shallow_delete_this_folder(
    monkeypatch,
    folder_contents_object_for_soft_delete,
    vdr_folder_subfolders,
    vdr_folder_files_list,
    mock_get_path,
    vdr_folder_detail,
    mock_object_with_generic_json_response,
):
    folder = folder_contents_object_for_soft_delete(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )
    monkeypatch.setattr(
        utils, "get_sub_folders_of_single_folder", vdr_folder_subfolders
    )
    monkeypatch.setattr(os.path, "join", mock_get_path)
    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)
    monkeypatch.setattr(utils, "get_files_in_single_folder", vdr_folder_files_list)
    monkeypatch.setattr(
        utils, "shallow_delete_single_folder", mock_object_with_generic_json_response
    )

    folder.prepare_folder()
    folder.shallow_delete_this_folder()


@pytest.mark.django_db
def test_folder_contents_for_hard_delete_iterate_over_and_permanently_delete_files(
    monkeypatch,
    folder_contents_object_for_hard_delete,
    vdr_folder_subfolders,
    vdr_folder_files_list,
    mock_get_path,
    vdr_folder_detail,
    mock_object_with_generic_json_response,
):
    folder = folder_contents_object_for_hard_delete(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )
    monkeypatch.setattr(
        utils, "get_sub_folders_of_single_folder", vdr_folder_subfolders
    )
    monkeypatch.setattr(os.path, "join", mock_get_path)
    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)
    monkeypatch.setattr(utils, "get_files_in_single_folder", vdr_folder_files_list)
    monkeypatch.setattr(
        utils, "permanently_delete_single_file", mock_object_with_generic_json_response
    )

    folder.prepare_folder()
    folder.iterate_over_and_permanently_delete_files()


@pytest.mark.django_db
def test_folder_contents_for_hard_delete_permanently_delete_this_folder(
    monkeypatch,
    folder_contents_object_for_hard_delete,
    vdr_folder_subfolders,
    vdr_folder_files_list,
    mock_get_path,
    vdr_folder_detail,
    mock_object_with_generic_json_response,
):
    folder = folder_contents_object_for_hard_delete(
        123, "root/next level/SiteName/Folder1", "SiteName/Folder1"
    )
    monkeypatch.setattr(
        utils, "get_sub_folders_of_single_folder", vdr_folder_subfolders
    )
    monkeypatch.setattr(os.path, "join", mock_get_path)
    monkeypatch.setattr(utils, "get_single_folder_details", vdr_folder_detail)
    monkeypatch.setattr(utils, "get_files_in_single_folder", vdr_folder_files_list)
    monkeypatch.setattr(
        utils,
        "permanently_delete_single_folder",
        mock_object_with_generic_json_response,
    )

    folder.prepare_folder()
    folder.permanently_delete_this_folder()
