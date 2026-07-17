#service is responsible for handling the business logic of the application. It interacts with the data layer (e.g., database) and provides methods to perform operations related to todos.

from typing import List
from app.schemas.todo import Todo

_todos_db = [] # data base simulation

def get_all_todos() -> List[Todo]:
    return _todos_db

def create_todo(todo_data: Todo) -> Todo:
    # Check if a todo with the same task already exists
    for todo in _todos_db:
        if todo.task.lower() == todo_data.task.lower():
            raise ValueError("Todo with this task already exists.")
    _todos_db.append(todo_data)
    return todo_data

def delete_todo(todo_id: int) -> bool:
    for i, todo in enumerate(_todos_db):
        if todo.id == todo_id:
            _todos_db.pop(i)
            return True
    return False
    