from fastapi import APIRouter

from app.api.endpoints import common, manage_auth, manage_user

api_router = APIRouter()


api_router.include_router(common.router, prefix="/common")
api_router.include_router(manage_auth.router, prefix="/auth")
api_router.include_router(manage_user.router, prefix="/manage-user")