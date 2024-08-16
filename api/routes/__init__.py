from fastapi import APIRouter

from .activity import router as activity_router
from .category import router as category_router
from .city import router as city_router
from .organizer import router as organizer_router
from .place import router as place_router
from .user import router as user_router



router = APIRouter()

router.include_router(activity_router, prefix="/activities", tags=["activity"])
router.include_router(category_router, prefix="/categories", tags=["category"])
router.include_router(city_router, prefix="/cities", tags=["city"])
router.include_router(organizer_router, prefix="/organizers", tags=["organizers"])
router.include_router(place_router, prefix="/places", tags=["place"])
router.include_router(user_router, prefix="/users", tags=["users"])

