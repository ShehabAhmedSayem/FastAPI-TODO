import os
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app_todo.db import SessionLocal
from app_todo.user.models import UserModel
from app_todo.user.serializers import TokenDataSerializer
from app_todo.user.crud import get_user_by_email


SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserModel:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid JWT",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credential_exception
        token_data = TokenDataSerializer(email=email)
    except JWTError:
        raise credential_exception
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credential_exception
    return user
