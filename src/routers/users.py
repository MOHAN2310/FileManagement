from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from model import Folder, User
from schema import UserCreate
from utils import get_folder_by_name, get_user_by_name


router = APIRouter(
    prefix="/users",
    tags=["UserOperations"]
)

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    root_folder = Folder(name=f"{user.username}_root", user_id=db_user.id)
    db.add(root_folder)
    db.commit()

    user_details = get_user_by_name(user_name=user.username, db=db)
    folder_details = get_folder_by_name(folder_name=root_folder.name, db=db)
    return JSONResponse(
        content={
            "message": "User has been created Sucessfully",
            "user": {"id": user_details.id,"name": user_details.username},
            "folder": {"rootfolder_id": folder_details.id, "name": folder_details.name}
        }
    )
