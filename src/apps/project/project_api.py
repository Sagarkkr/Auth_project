from fastapi import APIRouter, Depends
from src.apps.authentication.roles import admin_required, get_current_user

router = APIRouter()


