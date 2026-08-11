from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.todo import Todo, TodoCreate, TodoUpdate
from app.services import todo_service
from app.api.deps import get_db

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.get("/", response_model=List[Todo])
def get_todos(db: Session = Depends(get_db)):
    """
    Get all todos.
    """
    return todo_service.get_all_todos()

@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo_data: TodoCreate, db: Session = Depends(get_db)):
    """
    Create a new todo.
    """
    try:
        return todo_service.create_todo(db,todo_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    success = todo_service.delete_todo(todo_id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return None

@router.get("/", response_model=List[Todo])
def list_todos(
    skip: int = 0,
    limit: int = 10,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    return todo_service.get_all_todos(db, skip=skip, limit=limit, completed=completed)

@router.patch("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_data: TodoUpdate, db: Session = Depends(get_db)):
    return todo_service.update_todo(db, todo_id, todo_data)