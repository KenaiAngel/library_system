from typing import Annotated
from models.user import UserResponse
from datetime import timedelta, datetime, timezone
from jose import  jwt, JWTError
from dotenv import load_dotenv
from pathlib import Path
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

import os
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SOMETHING = os.getenv("SOMETHING")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(request:UserResponse, expires_delta:timedelta):
    encode = {'sub': request.email,'id': request.id, 'role':request.role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode['exp'] = expires

    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get('sub')
        id: int = payload.get('id')
        role: str = payload.get('role')

        if email is None or id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        return {'email': email, 'id': id, 'role': role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

user_dependency = Annotated[dict, Depends(get_current_user)]






