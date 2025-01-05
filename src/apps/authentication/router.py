from fastapi import APIRouter

from src.apps.authentication import auth_api

auth_router = APIRouter(prefix="/auth")

auth_router.include_router(auth_api.router)
