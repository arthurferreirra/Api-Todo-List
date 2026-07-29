from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.todo import Todo
from app.services import todo_service

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.get("/", response_model=List[Todo])
def get_todos():
    """
    Get all todos.
    """
    return todo_service.get_all_todos()

@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: Todo):
    """
    Create a new todo.
    """
    try:
        return todo_service.create_todo(todo)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    success = todo_service.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return None