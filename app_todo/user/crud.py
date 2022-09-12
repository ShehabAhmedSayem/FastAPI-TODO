from typing import Optional, List

from sqlalchemy.orm import Session

from app_todo.user.models import UserModel
from app_todo.user.serializers import UserSerializer, UserCreateSerializer
from app_todo.user.utils import hash_password


def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_all_users(db: Session) -> List[UserModel]:
    return db.query(UserModel).filter().all()


def add_user(db: Session, user_data: UserCreateSerializer) -> UserSerializer:
    hashed_password = hash_password(user_data.password)
    db_user = UserModel(
        email=user_data.email,
        last_name=user_data.last_name,
        first_name=user_data.first_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
