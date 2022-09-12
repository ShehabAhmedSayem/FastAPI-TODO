from typing import List, Optional

from pydantic import BaseModel
from pydantic import EmailStr

from app_todo.todo.serializers import TodoSerializer


class UserBase(BaseModel):
    email: EmailStr


class UserSerializer(UserBase):
    first_name: str
    last_name: str


class UserCreateSerializer(UserSerializer):
    password: str


class UserDetailSerializer(UserSerializer):
    todos: List[TodoSerializer]


class TokenSerializer(BaseModel):
    access_token: str
    token_type: str


class TokenDataSerializer(BaseModel):
    email: Optional[str] = None
