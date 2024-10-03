from pydantic import BaseModel, Field
from typing import List

class UserCreate(BaseModel):
    username: str = Field(
        ...,
        title="User name",
        description="Name of the user to be created",
        example="Mohan Raj B"
    )

class FolderCreate(BaseModel):
    name: str = Field(
        ...,
        title="Folder name",
        description="Name of the folder to be created",
        example="Folders"
    )
    user_id: int = Field(
        ...,
        title="User ID",
        description="This folder belongs to the UserID",
        example=7,
    )
    parent_folder_id: int = Field(
        None,
        title="Parent Folder ID",
        description="Parent folder of this folder",
        example=7,
    )

class FileCreate(BaseModel):
    name: str = Field(
        ...,
        title="File name",
        description="Name of the file to be created",
        example="Files",
    )
    folder_id: int = Field(
        ...,
        title="Folder ID",
        description="This File belongs the Folder",
        example=7,
    )

class FileResponse(BaseModel):
    id: int = Field(
        ...,
        title="File ID",
        description="Id of the File",
        example=7,
    )
    name: str = Field(
        ...,
        title="File name",
        description="Name of the File",
        example="Files",
    )

    class Config:
        from_attributes = True


class FolderResponse(BaseModel):
    id: int = Field(
        ...,
        title="Folder ID",
        description="Id of the Folder",
        example=7,
    )
    name: str = Field(
        ...,
        title="Folder name",
        description="Name of the Folder",
        example=7,
    )
    subfolders: List['FolderResponse'] = []
    files: List[FileResponse] = []

    class Config:
        from_attributes = True 