#schema will be the base of the project and will be used to validate the data that is sent to the API. It will also be used to serialize the data that is returned from the API.
from pydantic import BaseModel

class TodoBase(BaseModel):
    task: str

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    completed: bool = False

    class Config:
        from_attributes = True