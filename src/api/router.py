from api.endpoints import (
    health,
    users,
)
from fastapi import APIRouter

router = APIRouter()
router.include_router(health.router, prefix="", tags=["health"])
router.include_router(users.router, prefix="/users", tags=["users"])
