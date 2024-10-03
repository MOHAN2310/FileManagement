from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from model import File
from database import get_db
from schema import FileCreate
from utils import get_file, get_file_by_name, get_folder


router = APIRouter(
    prefix="/file",
    tags=["FileOperations"]
)

@router.post("/", response_model=FileCreate)
async def create_file(file: FileCreate, db: Session = Depends(get_db)):
    db_file = File(name=file.name, folder_id=file.folder_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    file_details = await get_file_by_name(file_name=db_file.name, db=db)
    return JSONResponse(
        content={
            "message": "Flie has been created Sucessfully",
            "file": {"id": file_details.id, "name": file_details.name}
        }
    )


@router.delete("/{file_id}")
async def delete_file(file_id: int, db: Session = Depends(get_db)):
    file = await get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    db.delete(file)
    db.commit()
    return JSONResponse(
        content={
            "message": "File has been deleted sucessfully",
            "file": {"id": file.id, "name": file.name}
        }
    )


@router.put("/{file_id}/rename")
async def rename_file(file_id: int, new_name: str, db: Session = Depends(get_db)):
    file = await get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file.name = new_name
    db.commit()
    msg = f"File rename was successful for {file.name}"
    return JSONResponse(
        content={
            "message": msg,
            "file": {"id": file.id, "name": file.name}
        }
    )


@router.put("/move-file/{file_id}")
async def move_file(file_id: int, new_folder_id: int, db: Session = Depends(get_db)):
    file = await get_file(file_id=file_id, db=db)
    new_folder = await get_folder(folder_id=new_folder_id, db=db)

    if not file:
        raise HTTPException(status_code=404, detail="File not found.")
    if not new_folder:
        raise HTTPException(status_code=404, detail="destination folder not found.")
    
    file.folder_id = new_folder.id
    msg = f"File {file.name} moved to the folder {new_folder.name}"
    db.commit()

    return JSONResponse(
        content={
            "message": msg,
            "file": {"id": new_folder.id, "name": new_folder.name}
        }
    )


