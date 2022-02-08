from typing import List

from pydantic import BaseModel


class VDRSite(BaseModel):
    id: int
    name: str
    owner_email: str
    owner_name: str
    created_date: str
    status: str
    active_document_size: int
    deleted_document_size: int
    total_size: int
    site_root_folder_id: int
    error: bool = 0


class VDRSiteList(BaseModel):
    site_count: int
    pages: int
    final_offset: int
    site_list: List[VDRSite]


class VDRSiteCategory(BaseModel):
    category_name: str


class VDRSiteModule(BaseModel):
    module_name: str


class VDRSiteDetail(BaseModel):
    id: int
    name: str
    description: str
    administrator_notes: str
    owner_email: str
    owner_name: str
    created_date: str
    start_date: str
    archived_date: str
    status: str
    active_document_size: int
    deleted_document_size: int
    total_size: int
    site_root_folder_id: int
    bidder_site: bool
    error: bool = 0
    modules: List[VDRSiteModule]
    categories: List[VDRSiteCategory]
    password_protected: bool
    two_factor_authentication: bool
    terms_and_conditions: bool
    ip_restriction: bool
    digital_rights_management: bool
