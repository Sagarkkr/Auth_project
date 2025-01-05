from fastapi import Depends, HTTPException
from jose import JWTError
from src.apps.authentication.auth import decode_jwt_token

def get_current_user(token: str = Depends(...)):
    try:
        payload = decode_jwt_token(token)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def admin_required(current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
