from base64 import decode
from models.security import TokenData
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security.oauth2 import OAuth2PasswordBearer
from models.user_signup_model import User, UserInDB
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from repositories import users as users_repo

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "cad899cf9d4c0c405c5aaeabcdbb76fa5bc320fc1ef7926769f3e7f03e831f4d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# password encryption
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# returns the token from a user (when used in a Depends)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(token, fake_users_db)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = decoded_payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_user(username: str):
    print(username)
    user = await users_repo.find_user(username)
    print(user)
    if user:
        return UserInDB(**user)


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Password hashing


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta]):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
