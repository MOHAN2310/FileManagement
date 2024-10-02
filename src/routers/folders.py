from fastapi import APIRouter


router = APIRouter(
    prefix="/Folder",
    tags=["FolderOperations"]
)

@router.post("/")
def create_folder():
    return True