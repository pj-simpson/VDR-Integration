import datetime

import requests
from allauth.socialaccount.models import SocialToken

from core.data_parsers.site_data_parsers import (
    parse_get_all_sites,
    parse_get_single_site,
)
from core.dataclasses.utility_dataclasses import VDRServiceError
from core.http_handlers.utils import get_setting


def get_all_sites(request_user, request_query_params=None):

    """
    Gets all sites from the VDR API

    Makes an http call to the External Service to get all the site for the user,
    sends the json response to the data parsing function.

    :param request_user, any query params(optional)
    :return: a data class for a list of the remote VDR sites.
    """
    VDR_BASEURL = get_setting("remote_system_base_url")

    if request_query_params:
        params = request_query_params.urlencode()
    else:
        params = ""

    access_token = SocialToken.objects.get(account__user=request_user)
    url = f"{VDR_BASEURL}/sites?{params}&limit=10"
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
        result = parse_get_all_sites(response.json())

    return result


def get_single_site(request_user, id: int):

    """
    Gets the detailed single site call from the VDR API

    Makes an http call to the External Collaborate Service to get a single site,
    sends the json response to the data parsing function.

    :param request_user, the remote_vdr site id
    :return: a data class for a single remote VDR site's details.
    """
    VDR_BASEURL = get_setting("remote_system_base_url")

    site_id = id

    access_token = SocialToken.objects.get(account__user=request_user)
    url = f"{VDR_BASEURL}/sites/{site_id}"
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
        result = parse_get_single_site(response.json())
    return result
