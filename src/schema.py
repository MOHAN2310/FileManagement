from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str

class FolderCreate(BaseModel):
    name: str
    user_id: int
    parent_folder_id: int = None

class FileCreate(BaseModel):
    name: str
    folder_id: int