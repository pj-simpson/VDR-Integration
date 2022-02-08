from core.dataclasses.file_and_folder_dataclasses import (
    VDRFile,
    VDRFileList,
    VDRFolder,
    VDRSubFolderList,
)


def parse_get_folder_details(json) -> VDRFolder:
    """

    Turn json of VDR Folder into Dataclass

    Takes a json of a vdr folder and parses them into our pydantic dataclasses.

    :param json: json object
    :return: pydantic dataclass for VDRFolder
    """

    folder = VDRFolder(
        id=json["id"],
        name=json["name"],
        parent_folder_id=json["parentFolderID"],
        location=json["location"],
    )
    return folder


def parse_get_single_folder_subfolders(json) -> VDRSubFolderList:

    """

    Turn json for a list of VDR Folders into Dataclass

    Iterates over a json of a vdr folder list and parses into our pydantic dataclass.

    :param json: json object
    :return: pydantic dataclass for VDRFolder List
    """

    folder_list = []
    for item in json["folder"]:
        folder = VDRFolder(
            id=item["id"],
            name=item["name"],
            parent_folder_id=item["parentFolderID"],
            location=item["location"],
        )
        folder_list.append(folder)

    pydantic_folder_list = VDRSubFolderList(subfolder_list=folder_list)
    return pydantic_folder_list


def parse_get_files_in_single_folder(json) -> VDRFileList:

    """
    Turn json for a list of VDR Files into Dataclass

    Iterates over a json of a vdr files list and parses into our pydantic dataclass.

    :param json: json object
    :return: pydantic dataclass for VDRFile List

    """

    file_list = []

    for item in json["file"]:
        file = VDRFile(
            id=item["id"],
            name=item["name"],
            type=item["type"],
            size=item["size"],
        )
        file_list.append(file)

    pydantic_file_list = VDRFileList(file_list=file_list)
    return pydantic_file_list
