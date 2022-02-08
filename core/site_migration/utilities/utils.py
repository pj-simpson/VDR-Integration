import os
from typing import List

import boto3
from django.conf import settings
from django.contrib.auth import get_user_model

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
from core.http_handlers.utils import get_setting
from reporting.utils import ReportWriter

User = get_user_model()


class FolderContents:
    """
    A class used to represent the Contents of a folder in the external VDR System

    ...

    Attributes
    ----------
    user : User object
        a user object representing the authenticated user interacting with the VDR Service
    folder_id : int
        the unique identifier of the folder in the VDR System
    local_path : str
        the location of this folder on the local server
    vdr_path : str
        the location of this folder in the VDR server
    folder_details: VDRFolder dataclass
        the details specific to this folder, stored in the VDR System
    subfolders: VDRSubfolderArray dataclass
        the subfolders of the folder
    files: VDRFileList dataclass
    report_id: used to initialize the report
    report: initialized from the report_id at the time of folder detail retrieval,  the Report writer object can be referenced to create report
        line entries relevant to the steps taken

    Methods
    -------
    _get_folder_details()
        Gets the details of the folder from VDR service

    _update_local_path()
        Updates the local_path attribute, relative to the servers static root + folder name

    _update_vdr_path()
        Updates the vdr_path attribute, appending on the folder's name

    _get_subfolders()
        Gathers the subfolders of the folder

    _get_files()
        Gathers the files contained within the folder

    prepare_folder()
        calls all the relevant 'praviate' methods in order to prepare the folder contents object for replication or
        deletion operations.

    has_files()
        Checks whether or not there are files in the Objects files attribute

    has_folders()
        Checks whether or not there are sub-folders in the Objects subfolders attribute



    """

    def __init__(
        self, user, folder_id, local_path=None, vdr_path=None, report_id: int = None
    ):

        self.user = User.objects.get(id=user)
        self.folder_id = folder_id
        self.local_path = local_path
        self.vdr_path = vdr_path
        self.folder_details = None
        self.subfolders = None
        self.files = None
        self.report_id = report_id
        self.report = None

    def _get_folder_details(self):
        self.folder_details = get_single_folder_details(self.user, self.folder_id)

    def _initialize_report_writer(self):

        if not self.report_id:
            self.report = ReportWriter(self.folder_details.name)
            self.report_id = self.report.report_id
        else:
            self.report = ReportWriter(
                self.folder_details.name, report_id=self.report_id
            )

    def _update_local_path(self):

        if not self.local_path:
            self.local_path = os.path.join(
                settings.MEDIA_ROOT, self.folder_details.name
            )
        else:
            self.local_path = os.path.join(self.local_path, self.folder_details.name)

    def _update_vdr_path(self):

        if not self.vdr_path:
            self.vdr_path = self.folder_details.name
        else:
            self.vdr_path = self.vdr_path + "/" + self.folder_details.name

    def _get_subfolders(self):
        self.subfolders = get_sub_folders_of_single_folder(self.user, self.folder_id)

    def _get_files(self):
        self.files = get_files_in_single_folder(self.user, self.folder_id)

    def prepare_folder(self):
        self._get_folder_details()
        self._initialize_report_writer()
        self._update_local_path()
        self._update_vdr_path()
        self._get_subfolders()
        self._get_files()

    def has_files(self):
        if self.files is not None:
            if len(self.files.file_list) > 0:
                return True
            else:
                return False
        else:
            return False

    def has_subfolders(self):
        if self.subfolders is not None:
            if len(self.subfolders.subfolder_list) > 0:
                return True
            else:
                return False
        else:
            return False


class FolderContentsForLocal(FolderContents):
    """
    A class used to represent the Contents of a folder in the VDR System, where we wish to replicate
    on the local Server

    Child of FolderContents object

    Methods
    -------
    iterate_over_and_write_files_to_local()
        For each file contained within the folder, download and write to the local server.

    write_folder_to_local()
        Creating the corresponding directory to this folder on the local server

    """

    def _get_local_file_path(self, file):
        file_name = file.name
        file_type = file.type
        file_and_extension = file_name + "." + file_type
        return os.path.join(self.local_path, file_and_extension)

    def _write_file_to_local(self, file, path):

        with open(path, "wb") as f:
            for chunk in file.iter_content(8192):
                f.write(chunk)

    def iterate_over_and_write_files_to_local(self):
        for file in self.files.file_list:
            local_new_file_path = self._get_local_file_path(file)
            file_id = file.id

            downloaded_file = download_single_file(self.user, file_id)
            self._write_file_to_local(downloaded_file, local_new_file_path)
            self.report.write_line(
                f"Currently creating {local_new_file_path} on the local server"
            )

    def write_folder_to_local(self):
        os.mkdir(self.local_path)
        self.report.write_line(
            f"Currently replicating {self.folder_details.name} on the local server"
        )


class FolderContentsForRemote(FolderContents):
    """
    A class used to represent the Contents of a folder in the VDR System, where we wish to replicate
    in the remote object storage location.

    Child of FolderContents object

    Attributes
    ----------
    s3_client : Client from the boto3 library
        a client object to interact with AWS S3.

    Methods
    -------
    iterate_over_and_write_files_to_remote()
        For each file contained within the folder, stream the file to the AWS s3 Bucket.

    write_empty_folder_to_remote()
        Creating the corresponding empty folder object in the AWS s3 Bucket.

    """

    def __init__(self, **kwargs):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=get_setting("aws_access_key_id"),
            aws_secret_access_key=get_setting("aws_secret_access_key"),
        )
        self.aws_bucket_name = get_setting("aws_bucket_name")
        super().__init__(**kwargs)

    def _get_remote_file_path(self, file):
        file_name = file.name
        file_type = file.type
        file_and_extension = file_name + "." + file_type
        return os.path.join(self.vdr_path + "/" + file_and_extension)

    def iterate_over_and_write_files_to_remote(self):

        for file in self.files.file_list:
            print(self.aws_bucket_name)
            vdr_new_file_path = self._get_remote_file_path(file)
            file_id = file.id

            downloaded_file = download_single_file(self.user, file_id)
            self.s3_client.upload_fileobj(
                downloaded_file.raw, self.aws_bucket_name, vdr_new_file_path
            )
            self.report.write_line(
                f"Currently replicating {vdr_new_file_path} to the remote storage location"
            )

    def write_empty_folder_to_remote(self):
        self.s3_client.put_object(
            Bucket=self.aws_bucket_name, Body="", Key=self.vdr_path
        )
        self.report.write_line(
            f"Currently replicating {self.vdr_path} to the remote storage location"
        )


class FolderContentsForSoftDelete(FolderContents):
    """
    A class used to represent the Contents of a folder in the VDR System, where we wish to move the folder
    and its contents to the recycle bin of the VDR

    Child of FolderContents object

    Methods
    -------
    iterate_over_and_shallow_delete_files()
        moves every file contained in this folder to the VDR site's 'deleted items' folder

    shallow_delete_this_folder()
        moves the folder in question to the VDR Site's deleted items folder.


    """

    def iterate_over_and_shallow_delete_files(self):
        for file in self.files.file_list:
            shallow_delete_single_file(self.user, file.id)
            self.report.write_line(f"Currently moving {file.name} to recycle bin")

    def shallow_delete_this_folder(self):
        shallow_delete_single_folder(self.user, self.folder_id)
        self.report.write_line(
            f"Currently moving {self.folder_details.name} to recycle bin"
        )


class FolderContentsForHardDelete(FolderContentsForSoftDelete):
    """
    A class used to represent the Contents of a folder in the VDR System, where we wish to permanently and irretrvably delete
     the folder and its contents to the out of the VDR


    Child of FolderContentsForSoftDelete object (we need to soft delete before hard deleting!)


    Methods
    -------


    iterate_over_and_permanently_delete_files()
        permanently deletes every file which was previously contained within this folder, but has been moved to the
        VDR Site's deleted items folder


    permanently_delete_this_folder()
        permanently deletes this folder out of the VDR Site's recycle bin.

    """

    def iterate_over_and_permanently_delete_files(self):
        for file in self.files.file_list:
            permanently_delete_single_file(self.user, file.id)
            self.report.write_line(f"Currently permanently deleting {file.name}")

    def permanently_delete_this_folder(self):
        permanently_delete_single_folder(self.user, self.folder_id)
        self.report.write_line(
            f"Currently permanently deleting {self.folder_details.name}"
        )
