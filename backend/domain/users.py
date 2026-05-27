from database.models import User
from models.user import UserRequest
from security.encrypt import hash_password, verify_password
from security.constants import ADMIN_ROLE, READER_ROLE

def add_user(user:UserRequest):
    hashed_password = hash_password(user.password)

    existing_user = User.get_or_none(User.email == user.email)
    if existing_user:
        return {'status': False, 'detail': 'A user with that email already exists.'}

    new_user = User.create(
        username=user.username,
        email=user.email,
        password = hashed_password,
        role = READER_ROLE,
        is_active = True
    )
    return {'status':True, 'data': new_user}

def authenticate_user(email:str, password:str):
    user = User.get_or_none(User.email == email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

