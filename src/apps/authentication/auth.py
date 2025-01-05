from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "3f32b38e185eff5cd172692bbbf9e5e3162d02609ff06e4ff98735810edb9324"
ALGORITHM = "HS256"

def create_jwt_token(user):
    payload = {
        "sub": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
