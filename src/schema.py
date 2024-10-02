from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str

class FolderCreate(BaseModel):
    name: str
    user_id: int
    parent_folder_id: int = None

class FileCreate(BaseModel):
    name: str
    folder_id: int

class FileResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class FolderResponse(BaseModel):
    id: int
    name: str
    subfolders: List['FolderResponse'] = []
    files: List[FileResponse] = []

    class Config:
        from_attributes = True 