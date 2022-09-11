from pydantic import BaseModel


class TodoBaseSerializer(BaseModel):
    text: str
    completed: bool


class TodoSerializer(TodoBaseSerializer):
    owner_id: int


class TodoDetailSerializer(TodoSerializer):
    id: int


class TodoUpdateSerializer(TodoBaseSerializer):
    id: int
