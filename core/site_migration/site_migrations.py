from typing import List, TypedDict

from celery import shared_task
from django.contrib.auth import get_user_model

from reporting.utils import ReportWriter

from .utilities.utils import (
    FolderContentsForHardDelete,
    FolderContentsForLocal,
    FolderContentsForRemote,
    FolderContentsForSoftDelete,
)

User = get_user_model()


@shared_task()
def recursive_site_builder_task(
    request_user_id: int,
    folder_id: int,
    local_path=None,
    vdr_path=None,
    report_id: int = None,
) -> None:

    """

    Downloads an entire site in the VDR system to the local server.

    Gets the details and contents of a Folder, iterating over the files and saving them to the local environment (after calculating the paths).
    Will recursively call itself for every subfolder.


    :param request_user_id: the unique identifier of the user in the VDR System making the call
    :param folder_id:  the unique identifier of the folder in the VDR System
    :param local_path: the path on the local server where the folder is located
    :param vdr_path: the path on the VDR system where the folder is located
    :param report_Id: the report to associate information about the task to
    :return: None
    """

    # prepare the current folder
    current_folder = FolderContentsForLocal(
        user=request_user_id,
        folder_id=folder_id,
        local_path=local_path,
        vdr_path=vdr_path,
        report_id=report_id,
    )
    current_folder.prepare_folder()
    current_folder.write_folder_to_local()

    if current_folder.has_files():
        current_folder.iterate_over_and_write_files_to_local()

    if current_folder.has_subfolders():
        for folder in current_folder.subfolders.subfolder_list:
            recursive_site_builder_task.delay(
                current_folder.user.id,
                folder.id,
                current_folder.local_path,
                current_folder.vdr_path,
                current_folder.report_id,
            )


@shared_task()
def recursive_remote_storage_site_builder_task(
    request_user_id: int,
    folder_id: int,
    local_path=None,
    vdr_path=None,
    report_id: int = None,
) -> None:

    """

    Replicates an entire site in the VDR system in an AWS S3 Bucket.

    Gets the details and contents of a Folder, iterating over the files and streaming them to the AWS bucket (after calculating the correct paths).
    Will recursively call itself for every subfolder.


    :param request_user_id: the unique identifier of the user in the VDR System making the call
    :param folder_id:  the unique identifier of the folder in the VDR System
    :param local_path: the path on the local server where the folder is located
    :param vdr_path: the path on the VDR system where the folder is located
    :return: None
    """

    current_folder = FolderContentsForRemote(
        user=request_user_id,
        folder_id=folder_id,
        local_path=local_path,
        vdr_path=vdr_path,
        report_id=report_id,
    )
    current_folder.prepare_folder()

    # handle empty folder
    if not current_folder.has_subfolders() and not current_folder.has_files():
        current_folder.write_empty_folder_to_remote()

    if current_folder.has_files():
        current_folder.iterate_over_and_write_files_to_remote()

    if current_folder.has_subfolders():
        for folder in current_folder.subfolders.subfolder_list:
            recursive_remote_storage_site_builder_task.delay(
                current_folder.user.id,
                folder.id,
                current_folder.local_path,
                current_folder.vdr_path,
                current_folder.report_id,
            )


class FolderInitiationDetails(TypedDict):
    folder_id: int
    vdr_path: str
    local_path: str
    report_id: int


@shared_task()
def recursive_site_shallow_delete_task(
    request_user_id,
    folder_id: int,
    local_path=None,
    vdr_path=None,
    report_id: int = None,
    branch_history: List[FolderInitiationDetails] = None,
) -> None:

    """

    Moves the contents an entire site in the VDR system to its deleted items folder.

    Given that calling a 'delete' operation on the root folder of a VDR can create a long running background task
        at the remote end (which can cause some issues), we are going to, instead, walk down each 'branch' of the
        folder tree, recording the details needed for folder initiation in a list of FolderInitiationDetails objects
        once we reach the end of a branch (a folder with no subfolders), we can safely delete the contents of that folder
        and then use the 'branch history' in reverse, to 'walk back up' the folder tree, deleting the files and folders
        on the way.

    :param request_user: the unique identifier of the user in the VDR System making the call
    :param folder_id:  the unique identifier of the folder in the VDR System
    :param local_path: the path on the local server where the folder is located
    :param vdr_path: the path on the VDR system where the folder is located
    :param branch_history: a list of all the folder_id's preceding this folder, in the folder tree
    :param report_id: the id for the report, which we want to write to for this task
    :return: None
    """

    current_folder = FolderContentsForSoftDelete(
        user=request_user_id,
        folder_id=folder_id,
        local_path=local_path,
        vdr_path=vdr_path,
        report_id=report_id,
    )

    current_folder.prepare_folder()
    folder_initial_values = FolderInitiationDetails(
        folder_id=folder_id,
        local_path=local_path,
        vdr_path=vdr_path,
        report_id=current_folder.report_id,
    )

    # Termination case for branch: no subfolders we want to delete everything from the branch

    if not current_folder.has_subfolders():

        if current_folder.has_files():
            current_folder.iterate_over_and_shallow_delete_files()

        # if the folder we are in is the root folder, do not delete - this can often cause issue in the remote VDR
        if current_folder.folder_details.parent_folder_id != 0:
            current_folder.shallow_delete_this_folder()

        if branch_history:
            # walk back up the folder tree!
            for entry in reversed(branch_history):
                folder = FolderContentsForSoftDelete(
                    user=request_user_id,
                    folder_id=entry["folder_id"],
                    vdr_path=entry["vdr_path"],
                    local_path=entry["local_path"],
                    report_id=entry["report_id"],
                )

                folder.prepare_folder()

                # check that we are not already dealing with a deleted folder - there will be branch crossover!
                if folder.folder_details.location != "Deleted items":

                    if folder.has_files():
                        folder.iterate_over_and_shallow_delete_files()

                    # second check to not delete the root folder
                    if folder.folder_details.parent_folder_id != 0:
                        folder.shallow_delete_this_folder()

    # If we are not at the end of the branch we just want to add the folder id to the branch history and recursively call the celery task on itself
    else:
        if branch_history:
            branch_history.append(folder_initial_values)
        else:
            branch_history = [folder_initial_values]

        for folder in current_folder.subfolders.subfolder_list:
            recursive_site_shallow_delete_task.delay(
                current_folder.user.id,
                folder.id,
                current_folder.local_path,
                current_folder.vdr_path,
                current_folder.report_id,
                branch_history,
            )


@shared_task
def recursive_site_permanent_delete_task(
    request_user_id,
    folder_id: int,
    local_path=None,
    vdr_path=None,
    report_id: int = None,
    branch_history: List[FolderInitiationDetails] = None,
) -> None:
    """

    Permanently deletes the contents an entire site in the VDR system.

    Given that calling a 'delete' operation on the root folder of a VDR can create a long running background task
        at the remote end (which can cause some issues), we are going to, instead, walk down each 'branch' of the
        folder tree, recording the details needed for folder initiation in a list of FolderInitiationDetails objects
        once we reach the end of a branch (a folder with no subfolders), we can safely delete the contents of that folder
        and then use the 'branch history' in reverse, to 'walk back up' the folder tree, deleting the files and folders
        on the way.

    :param request_user: the unique identifier of the user in the VDR System making the call
    :param folder_id:  the unique identifier of the folder in the VDR System
    :param local_path: the path on the local server where the folder is located
    :param vdr_path: the path on the VDR system where the folder is located
    :param branch_history: a list of all the folder_id's preceding this folder, in the folder tree
    :param report_id: the id for the report, which we want to write to for this task
    :return: None
    """

    current_folder = FolderContentsForHardDelete(
        user=request_user_id,
        folder_id=folder_id,
        local_path=local_path,
        vdr_path=vdr_path,
        report_id=report_id,
    )

    current_folder.prepare_folder()
    folder_initial_values = FolderInitiationDetails(
        folder_id=folder_id,
        local_path=local_path,
        vdr_path=vdr_path,
        report_id=current_folder.report_id,
    )

    # Termination case for branch: no subfolders, so we want to delete everything from the branch

    if not current_folder.has_subfolders():

        if current_folder.has_files():
            current_folder.iterate_over_and_shallow_delete_files()
            current_folder.iterate_over_and_permanently_delete_files()

        # if the folder we are in is the root folder, do not delete - this can often cause issue in the remote VDR
        if current_folder.folder_details.parent_folder_id != 0:
            current_folder.shallow_delete_this_folder()
            current_folder.permanently_delete_this_folder()

        if branch_history:
            # walk back up the folder tree!
            for entry in reversed(branch_history):
                folder = FolderContentsForHardDelete(
                    user=request_user_id,
                    folder_id=entry["folder_id"],
                    vdr_path=entry["vdr_path"],
                    local_path=entry["local_path"],
                    report_id=entry["report_id"],
                )

                folder.prepare_folder()

                # check that we are not already dealing with a deleted folder - there will be branch crossover!
                if folder.folder_details.location != "Deleted items":

                    if folder.has_files():
                        folder.iterate_over_and_shallow_delete_files()
                        folder.iterate_over_and_permanently_delete_files()

                    # second check to not delete the root folder:
                    if folder.folder_details.parent_folder_id != 0:
                        folder.shallow_delete_this_folder()
                        folder.permanently_delete_this_folder()

    # If we are not at the end of the branch we just want to add the folder's initial details to the branch history and recursively call the celery task on itself
    else:
        if branch_history:
            branch_history.append(folder_initial_values)
        else:
            branch_history = [folder_initial_values]

        for folder in current_folder.subfolders.subfolder_list:
            recursive_site_permanent_delete_task.delay(
                current_folder.user.id,
                folder.id,
                current_folder.local_path,
                current_folder.vdr_path,
                current_folder.report_id,
                branch_history,
            )
