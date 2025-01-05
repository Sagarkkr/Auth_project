from fastapi import APIRouter

from src.apps.project import project_api

project_router = APIRouter(prefix="/project")

project_router.include_router(project_api.router)
