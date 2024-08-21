from fastapi import APIRouter

from .activity_route import router as activity_router
from .category_route import router as category_router
from .city_route import router as city_router
from .organizer_route import router as organizer_router
from .place_route import router as place_router
from .user_route import router as user_router



router = APIRouter()

router.include_router(activity_router, prefix="/activities", tags=["activity"])
router.include_router(category_router, prefix="/categories", tags=["category"])
router.include_router(city_router, prefix="/cities", tags=["city"])
router.include_router(organizer_router, prefix="/organizers", tags=["organizers"])
router.include_router(place_router, prefix="/places", tags=["place"])
router.include_router(user_router, prefix="/users", tags=["users"])

