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
def vdr_site_list():
    def _vdr_site_list(*args, **kwargs):
        site_1 = VDRSite(
            id=123,
            name="Site 1",
            owner_email="person_1@example.com",
            owner_name="Person One",
            created_date="10 Jun 2019",
            status="Active",
            active_document_size=51207511,
            deleted_document_size=31921373,
            total_size=83128884,
            site_root_folder_id=1234,
        )
        site_2 = VDRSite(
            id=123,
            name="Site 2",
            owner_email="person_2@example.com",
            owner_name="Person One",
            created_date="11 Apr 2020",
            status="Active",
            active_document_size=51207511,
            deleted_document_size=31921373,
            total_size=83128884,
            site_root_folder_id=1234,
        )
        site_3 = VDRSite(
            id=123,
            name="Site 3",
            owner_email="person_3@example.com",
            owner_name="Person Three",
            created_date="02 Jan 2018",
            status="Active",
            active_document_size=51207511,
            deleted_document_size=31921373,
            total_size=83128884,
            site_root_folder_id=1234,
        )

        return VDRSiteList(
            site_count=123,
            pages=12,
            final_offset=120,
            site_list=[site_1, site_2, site_3],
        )

    return _vdr_site_list


@pytest.fixture
def vdr_site_detail():
    def _vdr_site_detail(*args, **kwargs):

        return VDRSiteDetail(
            id=1507,
            name="Peter's First Test Site",
            description="ppkdldrlos",
            administrator_notes="Read the knowledge base and try out anything that seems worthwhile trying.",
            owner_email="peter.simpson@example.com",
            owner_name="Sys Sys Admin App",
            created_date="12 Jun 2019",
            start_date="12 Jun 2019",
            archived_date="12 Jun 2019",
            status="Archived",
            active_document_size=7985171,
            deleted_document_size=613969,
            total_size=8599140,
            site_root_folder_id=7944,
            bidder_site=False,
            error=False,
            modules=[
                VDRSiteModule(module_name="home"),
                VDRSiteModule(module_name="activity"),
                VDRSiteModule(module_name="document"),
                VDRSiteModule(module_name="wiki"),
                VDRSiteModule(module_name="blog"),
                VDRSiteModule(module_name="task"),
                VDRSiteModule(module_name="event"),
                VDRSiteModule(module_name="isheet"),
                VDRSiteModule(module_name="qa"),
                VDRSiteModule(module_name="people"),
            ],
            categories=[VDRSiteCategory(category_name="None")],
            password_protected=False,
            two_factor_authentication=False,
            terms_and_conditions=False,
            ip_restriction=False,
            digital_rights_management=False,
        )

    return _vdr_site_detail


@pytest.fixture
def vdr_folder_detail():
    def _vdr_folder_detail(*args, **kwargs):

        return VDRFolder(
            id=1687,
            name="Just a folder name",
            parent_folder_id=6541,
            location="Parent Folder",
        )

    return _vdr_folder_detail


@pytest.fixture
def vdr_folder_subfolders():
    def _vdr_folder_subfolders(*args, **kwargs):

        folder_1 = VDRFolder(
            id=1687,
            name="Just a folder name",
            parent_folder_id=6541,
            location="Parent Folder",
        )
        folder_2 = VDRFolder(
            id=9845,
            name="Just another folder name",
            parent_folder_id=6541,
            location="Parent Folder",
        )

        return VDRSubFolderList(subfolder_list=[folder_1, folder_2])

    return _vdr_folder_subfolders


@pytest.fixture
def vdr_folder_files_list():
    def _vdr_folder_files_list(*args, **kwargs):

        file_1 = VDRFile(id=123, name="A File", type="png", size=456897)
        file_2 = VDRFile(id=54, name="Another File", type="jpeg", size=987451)

        return VDRFileList(file_list=[file_1, file_2])

    return _vdr_folder_files_list


@pytest.fixture
def vdr_file_detail():
    def _vdr_file_detail(*args, **kwargs):
        return VDRFile(id=123, name="A File", type="png", size=456897)

    return _vdr_file_detail
