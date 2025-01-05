from fastapi import APIRouter
from src.apps.authentication.router import auth_router
from src.apps.project.router import project_router


api_router_v1 = APIRouter(prefix="/api/v1")

# All app routers will be register here
api_router_v1.include_router(auth_router, tags=["Auth"])
api_router_v1.include_router(project_router, tags=["Project"])

