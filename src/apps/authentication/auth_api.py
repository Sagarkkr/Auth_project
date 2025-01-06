from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from src.apps.authentication.auth import create_jwt_token
from src.apps.authentication.schema import User
from src.apps.authentication import auth_dao

router = APIRouter()

@router.post("/register")
async def register(body:User):
    """
        Register user with their credentials
    """
    user = await auth_dao.fetch_user_details_dao(
        query={"username": body.model_dump().get('username')})
    if not user:
        user = await auth_dao.create_user_dao(body.model_dump())
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="User created successfully"
        )
    return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="User creation unsuccessful"
        )

@router.post("/login")
async def login(username: str, password: str):
    """
        User login endpoint with password check
    """
    user = await auth_dao.fetch_user_details_dao(query={"username": username})
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_jwt_token(user)
    return {"access_token": token}
