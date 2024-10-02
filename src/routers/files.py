from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from model import File
from database import get_db
from schema import FileCreate
from utils import get_file_by_name


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
