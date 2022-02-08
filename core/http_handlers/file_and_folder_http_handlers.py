import datetime

import requests
from allauth.socialaccount.models import SocialToken

from core.data_parsers.file_and_folder_data_parsers import (
    parse_get_files_in_single_folder,
    parse_get_folder_details,
    parse_get_single_folder_subfolders,
)
from core.dataclasses.utility_dataclasses import VDRServiceError
from core.http_handlers.utils import get_setting


def get_single_folder_details(request_user, folder_id: int):

    """
    Gets the details for a single folder from the VDR API

    Makes an http call to the External Service to get a single folder,
    sends the json response to the data parsing function.

    :param request_user: the user logged in during the request
    :param folder_id: int
    :return: a data class for a single folders details

    """
    VDR_BASEURL = get_setting("remote_system_base_url")

    access_token = SocialToken.objects.get(account__user=request_user)
    url = f"{VDR_BASEURL}/folder/{folder_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        result = VDRServiceError(
            message=response.text,
            status_code=response.status_code,
            endpoint=url,
            timestamp=datetime.datetime.now(),
        )
    else:
        result = parse_get_folder_details(response.json())

    return result


def get_sub_folders_of_single_folder(request_user, folder_id: int):

    """
    Gets the subfolders within a single folder from the VDR API

    Makes an http call to the External Service to get all the subfolders inside a single folder,
    sends the json response to the data parsing function.

    :param request_user: the user authenticated during the request
    :param folder_id: int
    :return: a data class for an array of single folders details
    """
    VDR_BASEURL = get_setting("remote_system_base_url")

    access_token = SocialToken.objects.get(account__user=request_user)
    url = f"{VDR_BASEURL}/subfolders/{folder_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        result = VDRServiceError(
            message=response.text,
            status_code=response.status_code,
            endpoint=url,
            timestamp=datetime.datetime.now(),
        )
    else:
        result = parse_get_single_folder_subfolders(response.json())
    return result


def get_files_in_single_folder(request_user, folder_id: int):

    """
    Gets the files contained within a single folder from the VDR API

    Makes an http call to the External Service to get all the files from inside a single folder,
    sends the json response to the data parsing function.

    :param request_user: the user authenticated during the request
    :param folder_id: int
    :return: a data class for an array of files
    """
    VDR_BASEURL = get_setting("remote_system_base_url")

    access_token = SocialToken.objects.get(account__user=request_user)
    url = f"{VDR_BASEURL}/files-in-folder/{folder_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        result = VDRServiceError(
            message=response.text,
            status_code=response.status_code,
            endpoint=url,
            timestamp=datetime.datetime.now(),
        )
    else:
        result = parse_get_files_in_single_folder(response.json())
    return result


def download_single_file(request_user, file_id: int):

    """

    Downloads a file from the VDR API

    Makes an http call to the External Service to download a single file,

    :param request_user: the user authenticated during the request
    :param file_id: int
    :return: the response object from the call to the http service
    """
    VDR_BASEURL = get_setting("remote_system_base_url")

    access_token = SocialToken.objects.get(account__user=request_user)
    url = f"{VDR_BASEURL}/download/{file_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code != 200:
        result = VDRServiceError(
            message=response.text,
            status_code=response.status_code,
            endpoint=url,
            timestamp=datetime.datetime.now(),
        )
    else:
        result = response
    return result


def shallow_delete_single_file(request_user, file_id: int):

    """

    Moves a file to it's sites deleted items folder

    Makes an http call to the External Service to shallow delete a single file,

    :param request_user: the user authenticated during the request
    :param file_id: int
    :return: the response object from the call to the http service
    """
    VDR_BASEURL = get_setting("remote_system_base_url")

    access_token = SocialToken.objects.get(account__user=request_user)
    url = f"{VDR_BASEURL}/soft-delete-file/{file_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        result = VDRServiceError(
            message=response.text,
            status_code=response.status_code,
            endpoint=url,
            timestamp=datetime.datetime.now(),
        )
        return result
    else:
        result = response
    return result



def permanently_delete_single_file(request_user, file_id: int):

    """

    Deletes a file out of it's sites deleted items folder and removes from the external system entirely. Irreversible.

    Makes an http call to the VDR Service to permanently delete a single file,

    :param request_user: the user authenticated during the request
    :param file_id: int
    :return: the response object from the call to the http service
    """
    VDR_BASEURL = get_setting("remote_system_base_url")

    access_token = SocialToken.objects.get(account__user=request_user)
    url = f"{VDR_BASEURL}/hard-delete-file/{file_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        result = VDRServiceError(
            message=response.text,
            status_code=response.status_code,
            endpoint=url,
            timestamp=datetime.datetime.now(),
        )
        return result
    else:
        result = response
    return result


def shallow_delete_single_folder(request_user, folder_id: int):

    """

    Moves a folder to it's sites deleted items folder

    Makes an http call to the External Service to shallow delete a single folder,

    :param request_user: the user authenticated during the request
    :param folder_id: int
    :return: the response object from the call to the http service
    """
    VDR_BASEURL = get_setting("remote_system_base_url")

    access_token = SocialToken.objects.get(account__user=request_user)
    url = f"{VDR_BASEURL}/soft-delete-folder/{folder_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        result = VDRServiceError(
            message=response.text,
            status_code=response.status_code,
            endpoint=url,
            timestamp=datetime.datetime.now(),
        )
        return result
    else:
        result = response
    return result


def permanently_delete_single_folder(request_user, folder_id: int):

    """

    Deletes a folder out of it's site's deleted items folder and removes from the system entirely. Irreversible.

    Makes an http call to the External Service to permanently delete a single folder,

    :param request_user: the user authenticated during the request
    :param folder_id: int
    :return: the response object from the call to the http service
    """
    VDR_BASEURL = get_setting("remote_system_base_url")

    access_token = SocialToken.objects.get(account__user=request_user)
    url = f"{VDR_BASEURL}/hard-delete-folder/{folder_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        result = VDRServiceError(
            message=response.text,
            status_code=response.status_code,
            endpoint=url,
            timestamp=datetime.datetime.now(),
        )
        return result
    else:
        result = response
    return result
