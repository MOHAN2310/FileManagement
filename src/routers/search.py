from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from schema import FolderResponse
from database import get_db
from utils import get_folder_by_name, get_file_by_name


router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

@router.post("/{name}")
def search_by_name(name: str, db: Session = Depends(get_db)):
    search_result = get_folder_by_name(folder_name=name, db=db)
    if search_result:
        msg = f"Folder {search_result.name} contains {len(search_result.subfolders)} subfolders and {len(search_result.files)} files."
        result_orm = FolderResponse.from_orm(search_result)
    else:
        search_result = get_file_by_name(file_name=name, db=db)
        if search_result:
            msg = f"File {search_result.name} contains."
            result_orm = FolderResponse.from_orm(search_result)
        else:
            raise HTTPException(status_code=404, detail="No record found for the given name.")
    
    return JSONResponse(
        content={
            "message": msg,
            "content": result_orm.dict()
        }
    )