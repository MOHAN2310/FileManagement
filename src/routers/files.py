from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from model import File
from database import get_db
from schema import FileCreate
from utils import get_file, get_file_by_name


router = APIRouter(
    prefix="/file",
    tags=["FileOperations"]
)

@router.post("/", response_model=FileCreate)
def create_file(file: FileCreate, db: Session = Depends(get_db)):
    db_file = File(name=file.name, folder_id=file.folder_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    file_details = get_file_by_name(file_name=db_file.name, db=db)
    return JSONResponse(
        content={
            "message": "Flie has been created Sucessfully",
            "folder": {"id": file_details.id, "name": file_details.name}
        }
    )


@router.delete("/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    file = get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    db.delete(file)
    db.commit()
    return JSONResponse(
        content={
            "message": "File has been deleted sucessfully",
            "folder": {"id": file.id, "name": file.name}
        }
    )


@router.put("/{file_id}/rename")
def rename_file(file_id: int, new_name: str, db: Session = Depends(get_db)):
    file = get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file.name = new_name
    db.commit()
    msg = f"File rename was successful for {file.name}"
    return JSONResponse(
        content={
            "message": msg,
            "folder": {"id": file.id, "name": file.name}
        }
    )

