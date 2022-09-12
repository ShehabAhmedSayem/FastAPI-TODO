from fastapi import FastAPI

from app_todo.user.views import user_router
from app_todo.todo.views import todo_router

app = FastAPI()

app.router.prefix = "/api/v1"

app.include_router(user_router, prefix="/users")
app.include_router(todo_router, prefix="/todos")
