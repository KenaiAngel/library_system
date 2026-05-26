from datetime import datetime
from pydantic import BaseModel

class UserResponse(BaseModel):
    id:int
    username:str
    email:str
    role:str

class UserRequest(BaseModel):
    username:str
    email:str
    password:str

class TokenResponse(BaseModel):
    access_token:str
    token_type:str
    user:UserResponse



