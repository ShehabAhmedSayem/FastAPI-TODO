from fastapi import FastAPI

from app_todo.views.

app = FastAPI()

app.router.prefix = "/api/v1/"

app.include_router()