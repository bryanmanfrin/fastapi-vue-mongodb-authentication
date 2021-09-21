from datetime import timedelta
from models.security import Token
from authentication.auth import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from models.user_signup_model import User, UserInDB, UserSignup
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from repositories import users as users_repo
from authentication import auth
from database import database

router = APIRouter(
    prefix='/auth',
    tags=['Authentication'],
)


@router.get("/items/")
async def read_items(user: User = Depends(auth.get_current_user)):
    return {"token": user}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    return current_user


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth.authenticate_user(form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup")
async def signup(user: UserSignup):
    hashed_pwd = auth.get_password_hash(user.password)
    userInDB = UserInDB(**user.__dict__, hashed_password=hashed_pwd)
    await users_repo.create_user(userInDB.dict())
