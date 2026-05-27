from datetime import datetime
from pydantic import BaseModel,field_validator
import re

class UserResponse(BaseModel):
    id:int
    username:str
    email:str
    role:str


class UserRequest(BaseModel):
    username:str
    email:str
    password:str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Field must not be blank")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(pattern, value):
            raise ValueError("Invalid email address")
        return value.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 6 or len(value) > 24:
            raise ValueError("Password must be between 6 and 24")
        return value


class TokenResponse(BaseModel):
    access_token:str
    token_type:str
    user:UserResponse



