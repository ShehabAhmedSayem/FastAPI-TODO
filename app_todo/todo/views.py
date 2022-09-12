from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app_todo.todo.crud import add_todo, update_todo, delete_todo, get_user_todos
from app_todo.dependencies import get_current_user
from app_todo.dependencies import get_db
from app_todo.user.models import UserModel
from app_todo.todo.serializers import (
    TodoBaseSerializer,
    TodoUpdateSerializer,
    TodoDetailSerializer,
)

todo_router = APIRouter()


@todo_router.get("", response_model=List[TodoDetailSerializer])
def get_my_todos_view(
    db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)
):
    todos = get_user_todos(db, current_user)
    return todos


@todo_router.post("", response_model=List[TodoDetailSerializer])
def add_todo_view(
    todo_data: TodoBaseSerializer,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    add_todo(
        db,
        current_user,
        todo_data,
    )
    todos = get_user_todos(db, current_user)
    return todos


@todo_router.put("", response_model=List[TodoDetailSerializer])
def update_todo_view(
    todo_data: TodoUpdateSerializer,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    update_todo(
        db,
        new_todo=todo_data,
    )
    todos = get_user_todos(db, current_user)
    return todos


@todo_router.delete("/{todo_id:int}", response_model=List[TodoDetailSerializer])
def delete_todo_view(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    delete_todo(db, todo_id)
    todos = get_user_todos(db, current_user)
    return todos
