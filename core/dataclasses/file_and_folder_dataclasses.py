from typing import List

from pydantic import BaseModel


class VDRFolder(BaseModel):
    id: int
    name: str
    parent_folder_id: int
    location: str


class VDRSubFolderList(BaseModel):
    subfolder_list: List[VDRFolder]


class VDRFile(BaseModel):
    id: int
    name: str
    type: str
    size: int


class VDRFileList(BaseModel):
    file_list: List[VDRFile]
