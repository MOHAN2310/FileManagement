from fastapi import APIRouter


router = APIRouter(
    prefix="/users",
    tags=["UserOperations"]
)

@router.post("/")
def create_user():
    return True