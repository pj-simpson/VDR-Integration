from builtins import KeyError, int, round
from math import ceil
from typing import List

from core.dataclasses.site_dataclasses import (
    VDRSite,
    VDRSiteCategory,
    VDRSiteDetail,
    VDRSiteList,
    VDRSiteModule,
)


def parse_get_all_sites(json) -> VDRSiteList:

    """
    Turn json of VDR Sites into Dataclass

    Takes a json of vdr sites and parses them into our pydantic dataclasses.
    Worth noting that confusingly the 'key' returned from the external service for their site list is 'site' singular

    :param: json object
    :return: vdr site list as Dataclass
    """

    site_list = []
    for item in json["site"]:
        site = VDRSite(
            id=item["id"],
            name=item["sitename"],
            owner_email=item["siteowner"]["email"],
            owner_name=item["siteowner"]["firstname"]
            + " "
            + item["siteowner"]["lastname"],
            created_date=item["createddate"],
            status=item["status"],
            active_document_size=item["rawsitesize"]["activedocumentsize"],
            deleted_document_size=item["rawsitesize"]["deleteddocumentsize"],
            total_size=item["rawsitesize"]["totalsize"],
            site_root_folder_id=item["sitefolderID"],
        )
        site_list.append(site)

    site_count = json["sitecount"]
    number_of_pages = ceil(site_count / 10)
    final_offset = round(site_count, -1)
    if final_offset > site_count:
        final_offset = final_offset - 10

    pydantic_site_list = VDRSiteList(
        site_count=site_count,
        pages=number_of_pages,
        final_offset=final_offset,
        site_list=site_list,
    )

    return pydantic_site_list


def parse_get_single_site(json) -> VDRSiteDetail:

    """
    Turn json of VDR single Site Detail call into Dataclass

    Takes a json of vdr site and parses it  into our pydantic dataclasses.

    :param: json object
    :return: vdr site detail as Dataclass
    """

    # Catch attributes of the vdr object which are not serialized if they are not there!

    try:
        admin_note = json["adminnote"]
    except KeyError:
        admin_note = ""
    try:
        site_description = json["sitedescription"]
    except KeyError:
        site_description = ""
    try:
        created_date = json["createddate"]
    except KeyError:
        created_date = ""
    try:
        start_date = json["startdate"]
    except KeyError:
        start_date = ""
    try:
        archived_date = json["archiveddate"]
    except KeyError:
        archived_date = ""

    site = VDRSiteDetail(
        id=json["id"],
        name=json["sitename"],
        owner_email=json["siteowner"]["email"],
        owner_name=json["siteowner"]["firstname"] + " " + json["siteowner"]["lastname"],
        created_date=created_date,
        status=json["status"],
        active_document_size=json["rawsitesize"]["activedocumentsize"],
        deleted_document_size=json["rawsitesize"]["deleteddocumentsize"],
        total_size=json["rawsitesize"]["totalsize"],
        site_root_folder_id=json["sitefolderID"],
        description=site_description,
        administrator_notes=admin_note,
        start_date=start_date,
        archived_date=archived_date,
        bidder_site=int(json["biddersite"]["enable"]),
        modules=parse_site_modules(json["module"]),
        categories=parse_site_categories(json["categories"]),
        password_protected=json["siteRestrictionType"]["passwordprotected"],
        two_factor_authentication=json["siteRestrictionType"][
            "twoFactorAuthentication"
        ],
        terms_and_conditions=json["siteRestrictionType"]["termsandconditions"],
        ip_restriction=json["siteRestrictionType"]["iprestrictedsite"],
        digital_rights_management=json["siteRestrictionType"]["drm"],
        error=0,
    )

    return site


def parse_site_modules(json) -> List[VDRSiteModule]:

    """
    Parse the  modules for a VDR Site

    Calls .items() on the JSON fragment for site modules, to more easily iterate over it. If a module is enabled,
    adds a VDRSiteModule pydantic data class to a list.

    json passed to this function is expected to look like this:

    {'home': {'enable': '0'}, 'activity': {'enable': '0', 'microblog': '0'}, 'document': {'enable': '1'}, 'wiki': {'enable': '1'},
    'blog': {'enable': '1'}, 'task': {'timelineview': '1', 'enable': '1'}, 'event': {'enable': '0'}, 'isheet': {'enable': '1'},
    'qa': {'enable': '0'}, 'people': {'enable': '1'}}


    :param: json object
    :return: a list of VDRSiteModule dataclasses
    """

    json_items = json.items()
    module_list = []
    for item in json_items:
        if item[1]["enable"] == "1":
            module_name = item[0]
            module = VDRSiteModule(module_name=module_name)
            module_list.append(module)
    return module_list


def parse_site_categories(json) -> List[VDRSiteCategory]:

    """
    Parse the  categories for a VDR Site

    Iterates over the JSON fragment for site categories and
    Adds a VDRSiteModule pydantic data class to a list.

    json passed to this function is expected to look like this:

    {'category': [{'id': '29', 'name': ' Test', 'httplink': None}]}



    :param: json object
    :return: a list of VDRSiteCategory dataclasses
    """
    category_list = []
    for item in json["category"]:
        category = VDRSiteCategory(category_name=item["name"])
        category_list.append(category)

    return category_list
