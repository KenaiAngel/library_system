from models.user import UserResponse
from datetime import timedelta, datetime, timezone
from jose import  jwt, JWTError
from dotenv import load_dotenv
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SOMETHING = os.getenv("SOMETHING")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(request:UserResponse, expires_delta:timedelta):
    print(SOMETHING)
    encode = {'sub': request.email,'id': request.id, 'role':request.role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode['exp'] = expires

    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)





