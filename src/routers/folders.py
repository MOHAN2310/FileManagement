from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db
from model import Folder
from schema import FolderCreate
from utils import get_folder_by_name, get_user


router = APIRouter(
    prefix="/Folder",
    tags=["FolderOperations"]
)

@router.post("/")
def create_folder(folder: FolderCreate, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=folder.user_id)
    db_folder = Folder(name=folder.name, parent_folder_id=folder.parent_folder_id, user_id=db_user.id)
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)

    folder_details = get_folder_by_name(folder_name=db_folder.name, db=db)
    return JSONResponse(
        content={
            "message": "Folder has been created Sucessfully",
            "folder": {"id": folder_details.id, "name": folder_details.name}
        }
    )
