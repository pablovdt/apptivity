from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_cities():
    return {"message": "List of cities"}
