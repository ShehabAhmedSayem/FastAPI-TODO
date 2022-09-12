from datetime import timedelta
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app_todo.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app_todo.user.crud import get_user_by_email, get_all_users, add_user
from app_todo.dependencies import get_db, get_current_user
from app_todo.user.models import UserModel
from app_todo.user.serializers import (
    UserSerializer,
    UserCreateSerializer,
    TokenSerializer,
)
from app_todo.user.utils import authenticate_user, create_access_token


user_router = APIRouter()


@user_router.get("", response_model=List[UserSerializer])
def users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return list(users)


@user_router.get("/{email:str}", response_model=UserSerializer)
def get_user(email: str, db: Session = Depends(get_db)) -> UserSerializer:
    user = get_user_by_email(db, email)
    if user:
        return user
    else:
        return {"message": "user not found"}, 404


@user_router.post("/signup", response_model=UserSerializer)
def sign_up(user_data: UserCreateSerializer, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="email exist",
        )
    new_user = add_user(db, user_data)
    return new_user


@user_router.post("/login", response_model=TokenSerializer)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user_data = authenticate_user(db, form_data.username, form_data.password)
    if not user_data:
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            detail="invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_expires_date = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.email},
        expires_delta=token_expires_date,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("me", response_model=UserSerializer)
def get_current_user(user_data: UserModel = Depends(get_current_user)):
    return user_data
