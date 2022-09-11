from typing import List

from pydantic import BaseModel
from pydantic import EmailStr

from app_todo.serializers.todo_serializers import TodoSerializer


class UserBase(BaseModel):
    email: EmailStr


class UserSerializer(UserBase):
    first_name: str
    last_name: str


class UserCreateSerializer(UserSerializer):
    password: str


class UserDetailSerializer(UserSerializer):
    todos: List[TodoSerializer]
