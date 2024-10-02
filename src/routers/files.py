from fastapi import APIRouter


router = APIRouter(
    prefix="/file",
    tags=["FileOperations"]
)

@router.post("/")
def create_file():
    return True