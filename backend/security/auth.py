from typing import Annotated
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from datetime import timedelta
from pydantic import EmailStr, ValidationError,TypeAdapter

from models.user import UserRequest, UserResponse, TokenResponse
from domain.users import add_user, authenticate_user
from security.jwt import create_access_token

email_adapter = TypeAdapter(EmailStr)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],

)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def signup(request: UserRequest):
    new_user = add_user(request)
    if not new_user['status']:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=new_user['detail']
        )
    token = create_access_token(new_user['data'],timedelta(minutes=60))

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            role=new_user.role
        )
    )

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    try:
        email = email_adapter.validate_python(form_data.username)
    except ValidationError:
        raise HTTPException(
            status_code=400,
            detail="Email inválido"
        )

    user = authenticate_user(email, form_data.password)
    token = create_access_token(user, timedelta(minutes=60))
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role
        )
    )








