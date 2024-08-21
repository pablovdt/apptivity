from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_activities():
    return {"message": "List of activities"}
