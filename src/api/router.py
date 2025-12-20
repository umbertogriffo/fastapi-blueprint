from api.endpoints import health, heroes, users
from fastapi import APIRouter

router = APIRouter()
router.include_router(health.router, prefix="", tags=["health"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(heroes.router, prefix="/heroes", tags=["heroes"])
