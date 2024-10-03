from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db
from model import Folder
from schema import FolderCreate, FolderResponse
from utils import get_folder, get_folder_by_name, get_user


router = APIRouter(
    prefix="/folders",
    tags=["FolderOperations"]
)

@router.post("/")
async def create_folder(folder: FolderCreate, db: Session = Depends(get_db)):
    db_user = await get_user(db=db, user_id=folder.user_id)
    db_folder = Folder(name=folder.name, parent_folder_id=folder.parent_folder_id, user_id=db_user.id)
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)

    folder_details = await get_folder_by_name(folder_name=db_folder.name, db=db)
    return JSONResponse(
        content={
            "message": "Folder has been created Sucessfully",
            "folder": {"id": folder_details.id, "name": folder_details.name}
        }
    )


@router.delete("/{folder_id}")
async def delete_folder(folder_id: int, db: Session = Depends(get_db)):
    folder = await get_folder(db, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found") 

    if folder.parent_folder_id:
        msg = "Folder has been deleted sucessfully"
        db.delete(folder)
        db.commit()
    else:
        msg = "Root Folder cannot be deleted"

    return JSONResponse(
        content={
            "message": msg,
            "folder": {"id": folder.id, "name": folder.name}
        }
    )


@router.put("/{folder_id}/rename")
async def rename_folder(folder_id: int, new_name: str, db: Session = Depends(get_db)):
    folder = await get_folder(db, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    folder.name = new_name
    db.commit()
    msg = f"Folder rename was successful for {folder.name}"
    return JSONResponse(
        content={
            "message": msg,
            "folder": {"id": folder.id, "name": folder.name}
        }
    )


@router.put("/{folder_id}/move")
async def move_folder(folder_id: int, new_folder_id: int, db: Session = Depends(get_db)):
    folder = await get_folder(folder_id=folder_id, db=db)
    new_folder = await get_folder(folder_id=new_folder_id, db=db)

    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found.")
    if not new_folder:
        raise HTTPException(status_code=404, detail="New folder not found.")
    if folder.parent_folder_id:
        msg = f"Folder {folder.name} moved to {new_folder.name}"
        folder.parent_folder_id = new_folder.id
    else:
        raise HTTPException(status_code=403, detail="Root folder cannot be modified.")
    db.commit()

    return JSONResponse(
        content={
            "message": msg,
            "folder": {"id": folder.id, "name": folder.name}
        }
    )


@router.get("/{folder_id}/contents")
async def fetch_folder_info(folder_id: int, db: Session = Depends(get_db)): 
    folder = await get_folder(folder_id=folder_id, db=db)
    if not folder:
        raise HTTPException(status_code=404, detail="Given folder not found in the database")
    
    folder_data = FolderResponse.from_orm(folder)
    
    msg = f"Folder {folder.name} contains {len(folder.subfolders)} subfolders and {len(folder.files)} files."
    return JSONResponse(
        content={
            "message": msg,
            "content": folder_data.dict()
        }
    )
