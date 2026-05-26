from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from datetime import timedelta

from models.user import UserRequest, UserResponse, TokenResponse
from domain.users import add_user, authenticate_user
from security.jwt import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["auth"],

)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def signup(request: UserRequest):
    new_user = add_user(request)
    token = create_access_token(new_user,timedelta(minutes=60))

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
    user = authenticate_user(form_data.username, form_data.password)
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








