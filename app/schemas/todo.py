#schema will be the base of the project and will be used to validate the data that is sent to the API. It will also be used to serialize the data that is returned from the API.
from pydantic import BaseModel
from typing import Optional

class TodoBase(BaseModel):
    task: str

class TodoUpdate(TodoBase):
    task: Optional[str] = None
    completed: Optional[bool] = None

class TodoCreate(TodoBase):
    task: str
    completed: bool = False

class TodoResponse(TodoBase):
    id: int
    task: str
    completed: bool
    owner_id: int

    class Config:
        from_attributes = True