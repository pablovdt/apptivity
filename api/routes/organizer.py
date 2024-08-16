from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_organizers():
    return {"message": "List of organizers"}
