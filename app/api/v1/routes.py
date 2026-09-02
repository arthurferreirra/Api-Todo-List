from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.todo import TodoResponse, TodoCreate, TodoUpdate
from app.services import todo_service
from app.api.deps import get_db, get_current_user
from app.models.user import UserModel

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """
    Get a specific todo by ID.
    """
    return todo_service.get_todo_by_id_and_user(db, todo_id= todo_id, user_id=current_user.id)

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo_data: TodoCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """
    Create a new todo.
    """
    try:
        return todo_service.create_todo(db,todo_data, owner_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    todo_service.delete_todo(db, todo_id=todo_id, user_id=current_user.id)
    return None

@router.get("/", response_model=List[TodoResponse])
def list_todos(
    skip: int = 0,
    limit: int = 10,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return todo_service.get_todos_by_user(db, user_id=current_user.id, skip=skip, limit=limit, completed=completed)

@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_data: TodoUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return todo_service.update_todo(db, todo_id=todo_id, user_id=current_user.id, todo_data=todo_data)