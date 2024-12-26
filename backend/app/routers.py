from fastapi import APIRouter, Depends
from app.controllers import (
    auth
)
# from app.dependencies.get_user import get_current_user

root_api_router = APIRouter(prefix="/api/v1")

root_api_router.include_router(auth.router, prefix="/auth", tags=["AUTH ENDPOINTS"])
